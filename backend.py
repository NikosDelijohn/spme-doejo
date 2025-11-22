# SPDX-License-Identifier: Apache-2.0

"""
backend.py

Flask backend for the SPME-DoEjo web application.

This module provides endpoints for:

1. `/query`   - Accepts a list of CAS numbers and returns possible PubChem CIDs and IUPAC names.
2. `/compute` - Accepts user-selected compounds and options, computes SPME Box-Behnken Design
               parameters, and returns a formatted HTML table of the experimental design.
3. `/`        - Serves the frontend HTML page for the compound selector interface.

The backend integrates:
- PubChemPy for retrieving compound information.
- pyDOE3 for Box-Behnken experimental design.
- Pandas for tabular data handling.
- Session storage for user-specific compound objects.

Additional Features:
- Handles errors gracefully and returns them in JSON.
- Supports ionic and high-viscosity options for SPME computation.
- Stores compounds in user session for further computations.
- Debug printing controlled by the `_DEBUG_` flag.
"""

# standard library
import secrets
# third-party
from flask import Flask, request, jsonify, render_template, session
import pandas
import pyDOE3
from pubchempy import Compound as pcpCompound
# first-party
from spme_doejo.compound import Compound
from spme_doejo.spme_conditions import SPMEConditions

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # New random key on each run

_DEBUG_ = True

def debug(*args, **kwargs):
    """
    Conditional debug print function.

    Prints the provided arguments to stdout only if the global _DEBUG_ flag is True.

    Parameters:
        *args: Variable length argument list to pass to print().
        **kwargs: Arbitrary keyword arguments to pass to print().
    """
    if _DEBUG_:
        print(*args, **kwargs)

# -------------------------
# Step 1: Receive CAS list and return all possible CID options
# -------------------------
@app.route("/query", methods=["POST"])
def query():
    """
    Handle CAS number queries and return possible PubChem CIDs and IUPAC names.

    Expects JSON input with the following structure:
        {
            "cas_list": ["64-17-5", "50-00-0", ...]
        }

    Returns:
        JSON array of objects, each representing a CAS number:
        [
            {
                "cas": "64-17-5",
                "options": [
                    {"cid": 702, "iupac_name": "ethanol"},
                    ...
                ]
            },
            {
                "cas": "50-00-0",
                "error": "Unable to retrieve compound"
            },
            ...
        ]

    Notes:
        - If multiple CIDs are found for a CAS number, all options are included.
        - If an error occurs for a CAS number, an "error" field is returned instead of "options".
        - Uses PubChemPy to fetch compound data.
        - Debug logging controlled by the global DEBUG function.
    """

    cas_list = request.json.get("cas_list", []) # type: ignore
    results = []

    debug("RECEIVED: cas_list", ",".join(cas_list))

    for cas in cas_list:
        try:
            debug("\tProcessing CAS: ", cas)
            sanitized_cas = Compound.sanitize_cas(cas)
            cids = Compound.cas_to_cid(sanitized_cas)
            iupac_names = [pcpCompound.from_cid(cid).iupac_name for cid in cids]

            results.append(
                {
                "cas": cas,
                "options": [{"cid": cid, "iupac_name": name} for
                            cid, name in zip(cids, iupac_names)]
                }
            )
        except (ValueError, TypeError) as e:  # only expected exceptions
            results.append({"cas": cas, "error": str(e)})
    debug("SENDING: ", results)
    return jsonify(results)

# -------------------------
# Step 2: User selects the correct CID per CAS, backend creates Compound objects
# -------------------------
@app.route("/compute", methods=["POST"])
def compute():
    """
    Compute SPME Box-Behnken Design (BBD) conditions for user-selected compounds and identify
    the appropriate fiber to be used.

    Expects JSON input with the following structure:
        {
            "selection": {
                "64-17-5": 702,
                "50-00-0": 712,
                ...
            },
            "properties": {
                "is_ionic": true,
                "has_high_viscocity": false
            },
            "center_points": 1  # optional, defaults to 1
        }

    Returns:
        JSON object with:
        {
            "status": "ok",
            "": <number_of_compounds_processed>,
            "table": "<HTML table of BBD design>" | null,
            "fiber": "<one of par.Fiber enum values>",
            "errors": [
                {"cas": "64-17-5", "cid": 702, "error": "..."},
                ...
            ]
        }

    Notes:
        - Creates Compound objects from the selected CIDs.
        - Computes SPME conditions: salt addition, extraction time & temperature, agitation rate.
        - Generates Box-Behnken Design using pyDOE3.
        - The number of center points can be adjusted via "center_points"; defaults to 1.
        - Errors for individual compounds are collected in the "errors" list.
        - Stores processed compounds in the user session for later use.
    """

    selection = request.json.get("selection", {}) # type: ignore
    additional_options = request.json.get("properties", {}) # type: ignore
    is_ionic = additional_options.get("is_ionic", False)
    has_high_viscocity = additional_options.get("has_high_viscocity", False)

    bbd_center_points = request.json.get("center_points", 1)  # type: ignore # now it works

    debug("RECEIVED: Ionic?: ", is_ionic, " High Viscocity?: ", has_high_viscocity)
    debug("RECEIVED: Center points ", bbd_center_points, type(bbd_center_points))
    compounds: list[Compound] = []
    errors: list[dict] = []

    for cas, selected_cid in selection.items():
        try:
            pubchem_compound_obj = pcpCompound.from_cid(selected_cid)
            iupac_name = pubchem_compound_obj.iupac_name
            bp_temp_in_k = Compound.get_compound_bp_in_kelvin(iupac_name) # type: ignore
            bp_temp_in_c = Compound.kelvin_to_celsius(bp_temp_in_k)

            compound = Compound(
                iupac_name, # type: ignore
                bp_temp_in_c,
                pubchem_compound_obj.xlogp, # type: ignore
                pubchem_compound_obj.molecular_weight # type: ignore
            )
            compounds.append(compound)
        except ValueError as e:
            errors.append({"cas": cas, "cid": selected_cid, "error": str(e)})

    # Store compounds in session for this user
    session["compounds"] = [comp.__dict__ for comp in compounds]

    # Only compute SPME if at least one compound succeeded
    table_html = None

    if compounds:

        conds = SPMEConditions(*compounds)

        conds.identify_fiber()
        conds.compute_salt_addition(is_ionic)
        conds.compute_extraction_time()
        conds.compute_extraction_temperature()
        conds.compute_agitation_rate(has_high_viscocity)

        try:
            factor_values = [
                conds.salt_addition.quantize(), # type: ignore
                conds.extraction_time.quantize(), # type: ignore
                conds.extraction_temp.quantize(), # type: ignore
                conds.agitation_rate.quantize() # type: ignore
            ]
            factor_values = [x for x in factor_values if x is not None]

            factor_map = [dict(zip([-1, 0, 1], factor_value)) for factor_value in factor_values]

            design = pandas.DataFrame(pyDOE3.bbdesign(len(factor_values),
                                      center=bbd_center_points),
                                      columns=conds.get_doe_header(),
                                      dtype=int)

            for i, col in enumerate(design.columns):
                design[col] = design[col].map(factor_map[i])

            design = design.astype(int)

            design.insert(0, "Experiment Number", range(1, len(design) + 1))

            table_html = design.to_html(
                classes="table table-striped table-bordered text-center",
                index=False,
                border=0,
                justify="center",
                table_id="doe-table"
            )

        except Exception as e:
            errors.append({"error": f"SPME computation failed: {e}"})

    debug("SENDING", table_html)

    return jsonify({
        "status": "ok",
        "": len(compounds),
        "table": table_html,
        "fiber": conds.fiber.value, # type: ignore
        "errors": errors
    })

# -------------------------
# Serve the frontend HTML
# -------------------------
@app.route("/")
def index():
    """
    Serve the main frontend HTML page for the SPME-DoEjo application.

    Returns:
        HTML page rendered from "frontend.html" template.

    Notes:
        - This is the main entry point for the web application.
        - The page includes CAS input, compound selection, property options,
          and Box-Behnken Design results.
        - Theme toggle (light/dark) is handled client-side via JavaScript.
    """
    return render_template("frontend.html")

if __name__ == "__main__":

    app.run(debug=True)
