from dataclasses import dataclass, field
from typing import List

@dataclass
class ValueData:
    label: str
    code: str

@dataclass
class FormValue:
    name: str
    values: List[ValueData] = field(default_factory=lambda: [ ] )