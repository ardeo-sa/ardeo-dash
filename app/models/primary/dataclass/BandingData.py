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
    lowerBand: float
    higherBand: float
    assignValue: float
    message: str
    assignColor: str
