#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""
parameters.py

This module defines all the necessary parameters for SPME Design-of-Experiments.
"""

# standard libary
import enum

class Fiber(enum.Enum):

    """Types of SPME fibers."""

    PDMS = "PDMS"
    PDMS_DVB = "PDMS-DVB"
    CAPPDMS_PEG_CW = "CAP-PDMS/PEG/CW"
    CW_DBV_PA = "CW/DBV/PA"
    DVB_CAR_PDMS = "DVB/CAR/PDMS"

class ExtractionTempCelsius(enum.Enum):

    """Extraction Temperatures."""

    THIRTY_TO_FORTY_C = "30-40 °C"
    FORTY_TO_SIXTY_C = "40-60 °C"
    SIXTY_TO_EIGHTY_C = "60-80 °C"

    def quantize(self, split: int = 3) -> list[float]:

        """
        Quantizes internal data into evenly spaced values.

        Args:
            split (int, optional): Number of quantization intervals. Defaults to 3.

        Returns:
            list[float]: A list of quantized floating-point values.
        """

        a, b = map(int, self.value.rstrip(" °C").split('-'))
        step = abs(a - b) / (split - 1)

        return [round(a + i * step, 2) for i in range(split)]

class ExtractionTimeMinutes(enum.Enum):

    """Extraction time (minutes)."""

    TEN_TO_TWENTY_M = "10-20 min"
    TWENTY_TO_THIRTY_M = "20-30 min"
    THIRTY_TO_SIXTY_M = "30-60 min"

    def quantize(self, split: int = 3) -> list[float]:

        """
        Quantizes internal data into evenly spaced values.

        Args:
            split (int, optional): Number of quantization intervals. Defaults to 3.

        Returns:
            list[float]: A list of quantized floating-point values.
        """

        a, b = map(int, self.value.rstrip(" min").split('-'))
        step = abs(a - b) / (split - 1)

        return [round(a + i * step, 2) for i in range(split)]

class NaClAdditionPct(enum.Enum):

    """NaCl addition percentages."""

    ZERO_PCT = "0%"
    ZERO_TO_TEN_PCT = "0-10%"
    TWENTY_TO_THIRTY_PCT = "20-30%"

    def quantize(self, split: int = 3) -> list[float] | None:

        """
        Quantizes internal data into evenly spaced values.

        Args:
            split (int, optional): Number of quantization intervals. Defaults to 3.

        Returns:
            list[float] | None: A list of quantized floating-point values if
            ``self.name`` is not "ZERO_PCT", otherwise ``None``.
        """

        retval = None

        if self.name != "ZERO_PCT":

            a, b = map(int, self.value.rstrip('%').split('-'))
            step = abs(a - b) / (split - 1)

            retval = [round(a + i * step, 2) for i in range(split)]

        return retval

class AgitationRateRPM(enum.Enum):

    """Agitation rates (rounds per minute)."""

    THREEH_TO_FIVEH_RPM = "300-500 rpm"
    FIVEH_TO_ONETH_RPM = "600-800 rpm"

    def quantize(self, split: int = 3) -> list[float]:

        """
        Quantizes internal data into evenly spaced values.

        Args:
            split (int, optional): Number of quantization intervals. Defaults to 3.

        Returns:
            list[float]: A list of quantized floating-point values.
        """

        a, b = list(map(int, self.value.rstrip(" rpm").split('-')))
        step = abs(a - b) / (split - 1)

        return [round(a + i * step, 2) for i in range(split)]
