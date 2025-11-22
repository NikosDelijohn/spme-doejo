#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""
compound.py

Class which extracts and holds only the required information gathered from Pubchempy and Chemical
packages for the purposes of our SPME condition computations.
"""

# standard libary
import re
import time

# dependencies
import requests
from thermo import Chemical

class Compound():
    """
    Represents a chemical compound with relevant physical-chemical properties.

    This class provides utility methods for CAS number validation,
    PubChem CID retrieval, temperature conversions, and boiling point
    extraction. It encapsulates the key properties of a compound,
    including IUPAC name, boiling point (in Celsius), octanol-water
    partition coefficient (XLogP), and molecular weight.

    Static Methods:
        sanitize_cas(cas: str) -> str:
            Validates and sanitizes a CAS number.
        cas_to_cid(cas: str) -> list[int]:
            Queries PubChem for CID(s) corresponding to a CAS number.
        kelvin_to_celsius(kelvin: float) -> float:
            Converts temperature from Kelvin to Celsius.
        get_compound_bp_in_kelvin(iupac_name: str) -> float:
            Retrieves the boiling point of a compound in Kelvin using
            the thermo.Chemical package.

    Attributes:
        iupac_name (str): The IUPAC name of the compound.
        boiling_point_celsius (float): Boiling point in degrees Celsius.
        xlogp (float): Octanol-water partition coefficient (XLogP).
        molecular_weight (int): Molecular weight in atomic mass units.

    Examples:
        >>> Compound.sanitize_cas("64-17-5")
        '64-17-5'

        >>> Compound.cas_to_cid("64-17-5")
        [702]

        >>> bp_k = Compound.get_compound_bp_in_kelvin("ethanol")
        >>> Compound.kelvin_to_celsius(bp_k)
        78.37

        >>> c = Compound("Ethanol", 78.37, -0.31, 46)
        >>> print(c)
        Ethanol | BP: 78.37°C | xLogP: -0.31 | MW: 46
    """
    @staticmethod
    def sanitize_cas(cas: str) -> str:
        """
        Sanitize, validate, and checksum-verify a CAS Registry Number.

        Validation steps:
        1. Type check — input must be a string.
        2. Format check — must match the CAS pattern: 2–7 digits, "-", 2 digits, "-", 1 digit.
        3. Structural check — digits must be fully parseable into integers.
        4. Checksum validation — computed checksum must match the final digit.

        Args:
            cas (str): The CAS number to validate (e.g., "64-17-5").

        Returns:
            str: The same CAS string if fully validated.

        Raises:
            ValueError: If:
                - `cas` is not a string.
                - The CAS does not match the required format.
                - The CAS contains non-numeric digit sections.
                - The computed checksum does not match the given checksum.

        Examples:
            >>> Compound.sanitize_cas("64-17-5")
            '64-17-5'

            >>> Compound.sanitize_cas("64-17-6")
            ValueError: [FAILED]: Checksum computation is invalid! Invalid CAS.
        """

        if not isinstance(cas, str):
            raise ValueError('[FAILED]: CAS must be a string!')

        if not re.fullmatch(r'[0-9]{2,7}-[0-9]{2}-[0-9]', cas):
            raise ValueError('[FAILED]: Invalid CAS format!')

        first_part, second_part, checksum = cas.split('-')

        try:
            digits = list(map(int, first_part)) + list(map(int, second_part))
            digits.reverse()
            checksum = int(checksum)
        except Exception as e:
            raise ValueError("[FAILED]: Malformed CAS entry!") from e

        _sum = 0
        for idx, val in enumerate(digits, start=1):
            _sum += idx*val

        if _sum % 10 != checksum:
            raise ValueError("[FAILED]: Checksum computation is invalid! Invalid CAS.")

        return cas

    @staticmethod
    def cas_to_cid(cas: str) -> list[int]:
        """
        Query PubChem (via PUG REST) to retrieve one or more CIDs associated with a CAS number.

        Validation & behavior:
        - Sends a GET request to PubChem.
        - Parses the response as one CID per line.
        - Converts all returned values into integers.
        - Any network, parsing, or API error is wrapped and re-raised as ValueError.

        Args:
            cas (str): A sanitized CAS Registry Number (e.g., "64-17-5").

        Returns:
            list[int]: A list of PubChem CIDs.
                    Will never be None; can be an empty list if PubChem returns no CIDs.

        Raises:
            ValueError: If:
                - The request times out.
                - A connection error occurs.
                - PubChem returns an error status.
                - The response cannot be parsed into integer CIDs.
                - Any general `requests` error occurs.

        Notes:
            PubChem PUG REST Documentation:
            https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest

        Example:
            >>> Compound.cas_to_cid("64-17-5")
            [702]
        """

        cas_rn_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/xref/rn/{cas}/cids/txt"
        print(f"Querying PubChem for CID of CAS: {cas}")

        try:

            time.sleep(0.1) # benign request

            response = requests.get(cas_rn_url, timeout=10)
            response.raise_for_status()

            response = list(map(int, response.text.splitlines()))

        except requests.exceptions.Timeout as e:
            raise ValueError(f"[FAILED]: Request timed out for CAS: {cas} ({e})") from e

        except requests.exceptions.ConnectionError as e:
            raise ValueError(f"[FAILED]: Connection error for CAS: {cas} ({e})") from e

        except requests.exceptions.RequestException as e:
            raise ValueError(f"[FAILED]: Error querying PubChem for CAS {cas}: {e}") from e

        return response

    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """
        Convert temperature from Kelvin to Celsius.

        Args:
            kelvin (float): Temperature in Kelvin.

        Returns:
            float: Temperature in Celsius.
        """
        return round(kelvin - 273.15, 2)

    @staticmethod
    def get_compound_bp_in_kelvin(iupac_name: str) -> float:
        """Return the boiling point of a compound in Kelvin.

        This function uses ``thermo.Chemical`` to look up the boiling point
        (``Tb``) of a compound given its IUPAC name. If the boiling point
        cannot be determined, an ``AssertionError`` is raised.

        Args:
            iupac_name (str): The IUPAC name of the compound.

        Returns:
            float: The boiling point in Kelvin.

        Raises:
            ValueError: If the boiling point temperature cannot be found for the given compound.

        Example:
            >>> Compound.get_compound_bp_in_kelvin("ethanol")
            351.44
        """
        temperature = Chemical(iupac_name).Tb

        if temperature is None:
            raise ValueError(f"Unable to find boiling point temperature for '{iupac_name}'!")

        return temperature

    def __init__(self, iupac_name: str, boiling_point_celsius: float, xlogp: float,
                  molecular_weight: int):
        self.iupac_name = iupac_name
        self.boiling_point_celsius = boiling_point_celsius
        self.xlogp = xlogp
        self.molecular_weight = molecular_weight

    def __repr__(self) -> str:
        """
        Official string representation of the Compound object.
        Intended for debugging and development.
        """
        return (f"Compound(iupac_name={self.iupac_name!r}, "
                f"boiling_point_celsius={self.boiling_point_celsius!r}, "
                f"xlogp={self.xlogp!r}, "
                f"molecular_weight={self.molecular_weight!r})")

    def __str__(self) -> str:
        """
        Informal string representation of the Compound object.
        Suitable for printing to the user.
        """
        return (f"{self.iupac_name} | BP: {self.boiling_point_celsius}°C | "
                f"xLogP: {self.xlogp} | MW: {self.molecular_weight}")
