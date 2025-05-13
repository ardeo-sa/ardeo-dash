from dataclasses import dataclass

@dataclass
class BandingData:
    lowerBand: float
    higherBand: float
    assignValue: float
    message: str
    assignColor: str
