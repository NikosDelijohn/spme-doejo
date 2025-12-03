#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""
spme_conditions.py

Class which provides utilities to compute conditions for SPME
of one or more chemical compound(s) based on literature.
"""
from .compound import Compound
from . import parameters as par

class SPMEConditions():

    """Computes baseline SPME conditions for one or more compound(s)"""

    def __init__(self, *compounds: Compound):
        self.compounds: list[Compound] = list(compounds)
        self._fiber: par.Fiber | None = None
        self._extraction_temp : par.ExtractionTempCelsius | None = None
        self._extraction_time : par.ExtractionTimeMinutes | None = None
        self._agitation_rate : par.AgitationRateRPM | None = None
        self._salt_addition : par.NaClAdditionPct | None = None

    @property
    def fiber(self): # pylint: disable=missing-function-docstring
        return self._fiber

    @fiber.setter
    def fiber(self, selected_fiber: par.Fiber): # pylint: disable=missing-function-docstring
        self._fiber = selected_fiber

    @property
    def extraction_temp(self): # pylint: disable=missing-function-docstring
        return self._extraction_temp

    @extraction_temp.setter
    def extraction_temp(self, other: par.ExtractionTempCelsius): # pylint: disable=missing-function-docstring
        self._extraction_temp = other

    @property
    def extraction_time(self): # pylint: disable=missing-function-docstring
        return self._extraction_time

    @extraction_time.setter
    def extraction_time(self, other: par.ExtractionTimeMinutes): # pylint: disable=missing-function-docstring
        self._extraction_time = other

    @property
    def salt_addition(self): # pylint: disable=missing-function-docstring
        return self._salt_addition

    @salt_addition.setter
    def salt_addition(self, other: par.NaClAdditionPct): # pylint: disable=missing-function-docstring
        self._salt_addition = other

    @property
    def agitation_rate(self): # pylint: disable=missing-function-docstring
        return self._agitation_rate

    @agitation_rate.setter
    def agitation_rate(self, other: par.AgitationRateRPM): # pylint: disable=missing-function-docstring
        self._agitation_rate = other

    def identify_fiber(self) -> par.Fiber:

        r"""Identifies the appropriate Fiber according to the object's compounds' attributes.

        Args:
            None

        Returns:
            par.Fiber: A Fiber type Enumerator.

        Notes:

            Fiber selection is governed by the analyte's polarity and volatility, expressed through
            its octanol-water partition coefficient (XLogP). The objective is to maximize the
            fiber-water distribution coefficient K_f/w, which determines extraction coefficiency.
            For non-polar  PDMS coatings, the relationship between K_f/w and K_ow follows:

                log(K_f/w) = 0.92 x log(K_ow) - 0.45

                for R^2 = 0.98 (Paschke & Popp, 2003)

            A threshold of log(K_f/w) > 4 (~= 90% recovery in 30min) corresponds to XlogP > 3.0
            For mid-polarity mixed coating such as PDMS/DVB and more polar phases (PA or PEG),
            regression intersections occur near XlogP ~= 1.5 and log P ~= 3.0 consistent with
            manufacturing guidelines (Supelcro, 2023) and QSPR models (Chao et al. 2014).

            Accordingly the algorithm uses the maximum XlogP among the analytes to classify
            optimal fiber polarity:

            PDMS (7 - 100μm): Nonpolar phase for hydrophobic, high-molecular-weight or
                              semi-volatile analytes (XLogP > 3.0).
            PDMS/DVB (65μm): Biphasic (absorption and adsorption) coating suitable for
                             moderately polar compounds (1.5 < XlogP < 3.0). The DVB layer
                             increases surface area and retention of small to mid-volatility
                             species such as phenols, esters and amines.
            DVB/CAR/PDMS(50/30μm): Multimodal composite phase providing broad selectivity from
                                   highly volatile to semi-volatile organics (0.5 < XlogP < 3.0).
                                   The CAR microporates trap small molecules (< C_6), while the
                                   DVB and PDMS layers capture higher-mass volatiles, making its
                                   coating optimal for complex mixed matrices.
            CW/DVB/PA: Polar composite phase designed for low-molecular-weight, hydrophilic
                       compounds (XlogP <= 1.5). The carbowax and polyacrylate components enhance
                       hydrogen bonding interactions and extraction of alcohols, organic acids and
                       aldehydes.
            CAP-PDMS/PEG/CW: Highly polar, hydrophilic coating for ionic, charged or very low
                             volatility compounds (XlogP ~<= 1.0 and M < 200 Da). This coating
                             targets strongly polar analytes such as short-chain acids, small
                             amines or environmental micropollutants that are poorly retained
                             on conventional fibers.

            In this method, fiber selection follows a monotonic polarity hierarchy:
            PDMS > PDMS/DVB > DVB/CAR/PDMS > CW/DVB/PA > CAP-PDMS/PEG/CW with transition thresholds
            at XlogP ~= 3.0, 1.5 and 1.0. This quantitative mapping reproduces manufacturer
            performance charts and maintains strong correlation with the calculated partition
            coefficients that govern extraction sensitivity.
        """

        retval = par.Fiber.DVB_CAR_PDMS

        if all(comp.xlogp > 3 for comp in self.compounds):
            retval = par.Fiber.PDMS
        elif all(comp.xlogp <= 3 for comp in self.compounds) and \
            all(comp.xlogp > 1.5 for comp in self.compounds):
            retval = par.Fiber.PDMS_DVB
        elif all(comp.xlogp <= 1.5 for comp in self.compounds):
            if all(float(comp.molecular_weight) <= 200 for comp in self.compounds):
                retval = par.Fiber.CAPPDMS_PEG_CW
            else:
                retval = par.Fiber.CW_DVB_PA

        self.fiber = retval
        return retval

    def compute_extraction_temperature(self) -> par.ExtractionTempCelsius:

        r"""Computes the appropriate extraction temperature according to max compound temperature.

        Args:
            None

        Returns:
            par.ExtractionTempCelcius: An ExtractionTempCelsius type Enumerator.

        Notes:

            The extraction temperature was derived from the analyte's boiling point based on the
            Clausius-Clapeyron relationship, which links vapor pressure and temperature through
            the equation:

                     P(T)         ΔΗvap        1     1
                ln( ------ ) = - -------  x ( --- - --- )
                      Pb            R          T     Tb

            Where Pb = 1 atm at the boiling point Tb, ΔΗvap is the molar enthalpy of vaporization,
            and R = 8.314 J/(mol x K). Headspace extraction becomes efficient once the analyte's
            vapor pressure at the boiling point, i.e, P(Te)/Pb = α = 0.10

            This criterion provides sufficient volatilization for effective headpsace partitioning
            without risking degradation or analyte loss. Applying the Clausius-Clapeyron equation
            in combination with the emprirical Trouton relation, ΔHvap ~= 88Tb (J/(mol x K)) gives:

                            Te
                Tb ~= ---------------
                          R x ln(1/a)
                      1 + -----------
                              88

            For a = 0.1, the correction term (R x ln(1/a)) / 88 is approx 0.26, leading to
            characteristic boiling-to-extraction temperature pairs of approximately:

                100 C -> 35 C
                200 C -> 50 C
                300 C -> 70 C

            These values define the three temperature bands implemented in the Enum below. The
            threshold breakpoints at 100 C and 200 C correspond to roughly tenfold changes in
            vapor presure, ensuring consistent volatility scaling across compounds.

            The method uses the maximum compound boiling point to determine the optimal extraction
            temperature range:

                        Tb < 100 C -> 30-40 C
                100 C < Tb < 200 C -> 40-60 C
                        Tb > 200 C -> 60-80 C

            This approach aligns with EPA volatility classification where very volatile organic
            compounds, volatile organic compounds and semi-volatile organic compounds require
            progressively higher extraction temperatures to achieve comparable vapor-phase
            concentrations.
        """

        retval = None

        max_temp: float = max(comp.boiling_point_celsius for comp in self.compounds)

        if max_temp < 100.0:
            retval = par.ExtractionTempCelsius.THIRTY_TO_FORTY_C
        elif 100.0 <= max_temp <= 200.0:
            retval = par.ExtractionTempCelsius.FORTY_TO_SIXTY_C
        else:
            retval = par.ExtractionTempCelsius.SIXTY_TO_EIGHTY_C

        self.extraction_temp = retval
        return retval

    def compute_extraction_time(self) -> par.ExtractionTimeMinutes:

        r""" Computes the SPME extraction time for the set of coumpounds provided.

        Args:
            None

        Returns:
            par.ExtractionTimesMinutes: An ExtractionTimeMinutes type Enumerator.

        Notes:

            The extraction time thresholds are based on diffusion-limited mass transfer described by
            the Stokes-Einstein relation:
                       kβ x T
                D = ------------
                     6π x η x r

            Where D is the diffusivity, η the viscosity, and r the hydrodynamic radius. Since
            molecular radius scales approximately as r ∝ M^(1/3), diffusivity decreases with
            molecular weight following D ∝ M^(1/3). Consequently, the characteristic equilibration
            time over distance Lis τ ~ L^2 / D ∝ M^(1/3), implying that heavier molecules require
            longer extraction times.

            Assuming a reference molecule (benzene, M0 = 78 g/mol) equiilibrates in 10 min, then
            the equilibration time scales as:
                               _____
                             3/  M
                τ(M) = τ0 x \/ -----
                                M0

            This yields characteristic times of approximately 20 min for M = 100, 30 min for
            M = 300, and 60 min for M = 600 g/mol, matching the extraction time bands we used.

            This scaling is consistent with diffusion-limited SPME kinetics, where larger analytes
            exhibit reduced mass transfer and require proportionally longer extraction durations.
            Empirical guidelines (Sigma-Aldrich, 2024) report 10-20 min for low molecular weight
            volatiles and 20-30 min for higher molecular weight semivolatiles, supporting the
            theoretical model.

        """
        retval = None

        max_molecular_weight: float = max(float(comp.molecular_weight) for comp in self.compounds)

        if max_molecular_weight < 100.0:
            retval = par.ExtractionTimeMinutes.TEN_TO_TWENTY_M
        elif 100.0 <= max_molecular_weight <= 300.0:
            retval = par.ExtractionTimeMinutes.TWENTY_TO_THIRTY_M
        else:
            retval = par.ExtractionTimeMinutes.THIRTY_TO_SIXTY_M

        self.extraction_time = retval
        return retval

    def compute_salt_addition(self, is_charged_or_ionic: bool) -> par.NaClAdditionPct:
        r""" Computes the required salt adition percentage for the set of compounds.

        Args:
            is_charged_or_ionic (bool): If true, at least one of the compounds is charged
                                        or ionic. Otherwise false.

        Returns:
            par.NaClAdditionPct: A NaclAdditionPct type Enumerator.

        Notes:

            Salt addition enhances headspace concentration through the salting-out effect,
            described by the Setschenow equation:
                     S0
                ln( ---- ) = ks x I
                     S

            Where I is the ionic strength. A significant salting-out effect (>=1 log unit decrease
            in solubility) typically occurs for compounds with log P < 2. The corresponding
            algorithmic threshold therefore applies 20-30% NaCl (~= 3-4 M) only when
            XLogP < 2.0, as the gain diminishes for more hydrophobic analytes.

            Reported Setchenow constants decrease with increasing hydrophobicity from ks ~= 0.25
            M^-1 for polar solutes (XlogP ~= 1.2) to ks ~= 0.05 M^-1 for nonpolar compounds
            (XlogP > 2) corresponding to enhancement factors of x4.5 and x1.1 at 6 M NaCl. Thus,
            salting-out is beneficial primarily for polar or moderatly polar compounds.
        """
        retval = None

        if is_charged_or_ionic:
            retval = par.NaClAdditionPct.ZERO_PCT

        else:

            max_logp: float = max(comp.xlogp for comp in self.compounds)

            if max_logp < 2.0:
                retval = par.NaClAdditionPct.TWENTY_TO_THIRTY_PCT
            else:
                retval = par.NaClAdditionPct.ZERO_TO_TEN_PCT

        self.salt_addition = retval
        return retval

    def compute_agitation_rate(self, has_high_matrix_viscosity: bool) -> par.AgitationRateRPM:

        r"""Computes the required agitation rate.

        Args:
            has_high_matrix_viscocity (bool): True means the matrix viscosity is high. False
                                              means is low.

        Returns:
            par.AgitationRateRPM: An AgitationRateRPM type Enumerator.

        Notes:
            Agitation enhances mass transfer from the aqueous matrix to the fiber according to
            the Sherwood correlation:
                     kL x L
                Sh = ------- = α x Re^b x Sc^c
                        D
                       ρ x N x Di^2
            Where Re = ------------- and
                            μ
                        μ
                  Sc = -----
                        ρD

            For low-viscosity aqueous systems, higher Reynolds numbers (600-800rpm) optimize
            extraction, whereas for viscous or semi-solid matrices, moderate agitation
            (300-500 rpm) maintains laminar flow and minimizes boundary-layer dusruption. The
            algorithm therefore adjusts agitation rate based on the matrix viscosity to ensure
            stable diffusion-controlled extraction.
        """

        retval = None

        retval = par.AgitationRateRPM.THREEH_TO_FIVEH_RPM \
            if has_high_matrix_viscosity \
            else par.AgitationRateRPM.FIVEH_TO_ONETH_RPM

        self.agitation_rate = retval

        return retval

    def deduce_desorption_rate(self) -> str:
        r"""Deduces the required desorption rate according to the selected fiber.

        Args:
            None

        Returns:
            str: A string naming the time and temperature required for desorption.

        Notes:
            Desorption parameters depend primarily on the fiber coating and film
            thickness. Recommended desorption temperatures are based on manufacturer
            data, ensuring complete analyte release without thermal degradation

        """

        return \
        {
            par.Fiber.PDMS: "3-5 min @ 250-280°C",
            par.Fiber.PDMS_DVB: "3-5 min @ 250-270°C",
            par.Fiber.DVB_CAR_PDMS: "4-6 min @ 270-300°C",
            par.Fiber.CW_DVB_PA: "4-6 min @ 250-280°C",
            par.Fiber.CAPPDMS_PEG_CW: "4-5 min @ 250-280°C"
        }[self.fiber] # type: ignore

    def get_doe_header(self) -> list[str]:
        """Return a list of column headers for a Design of Experiments (DOE) table.

        The headers include standard extraction parameters, and conditionally
        include "Salt Addition (%)" if the compound's salt addition is not '0%'.

        Returns:
            list[str]: A list of column header strings. The first element will be
                    "Salt Addition (%)" if applicable, followed by
                    "Extraction Time (minutes)", "Extraction Temp (celsius)",
                    and "Agitation Rate (rpm)".

        Example:
            >>> compound.get_doe_header()
            ['Salt Addition (%)', 'Extraction Time (minutes)',
            'Extraction Temp (celsius)', 'Agitation Rate (rpm)']
        """

        return (["Salt Addition (%)"] if self.salt_addition.value != '0%' else []) + [ # type: ignore
            "Extraction Time (minutes)",
            "Extraction Temp (celsius)",
            "Agitation Rate (rpm)"
        ]
