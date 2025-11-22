from .compound import Compound
from .parameters import (
    Fiber,
    ExtractionTempCelsius,
    ExtractionTimeMinutes,
    NaClAdditionPct,
    AgitationRateRPM
)
from .spme_conditions import SPMEConditions

__version__ = "0.1.0"

__all__ = ["Compound",
           "Fiber",
           "ExtractionTempCelsius",
           "ExtractionTimeMinutes",
           "NaClAdditionPct",
           "AgitationRateRPM",
           "SPMEConditions"]

__author__ = (
    "Laboratory of Analytical Chemistry, School of Chemistry, "
    "AUTH Thessaloniki, Greece, 54124"
)
__email__ = "info@seplab.gr"

__license__ = "Apache 2.0"
