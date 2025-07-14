"""
This module defines the BandingData dataclass used for value classification or scoring.

The BandingData class models a numeric range (band) with associated metadata such as
an assigned value, a message, and a color code. It can be used in systems involving
threshold evaluation, visual indicators (e.g., charts), or score interpretation.
"""
from dataclasses import dataclass

@dataclass
class BandingData:
    """
       Represents a data band range used for classification or scoring purposes.

       Attributes:
           lowerBand (float): The lower bound of the band range (inclusive).
           higherBand (float): The upper bound of the band range (inclusive).
           assignValue (float): The value assigned when a data point falls within this band.
           message (str): A descriptive message associated with this band.
           assignColor (str): A color code or name used to represent this band visually (e.g., "red", "#FF0000").
       """
    lower_band: float
    higher_band: float
    assign_value: float
    message: str
    assign_color: str
