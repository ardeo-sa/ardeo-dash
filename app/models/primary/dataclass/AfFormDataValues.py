from dataclasses import dataclass, field
from typing import List

@dataclass
class ValueData:
    """
      Represents a single value item with a human-readable label and an associated code.

      Attributes:
          label (str): The display label for the value (e.g., "Male", "Female").
          code (str): The code representing the value (e.g., "M", "F").
      """
    label: str
    code: str

@dataclass
class FormValue:
    """
        Represents a named field and a list of selectable values for a form.

        Attributes:
            name (str): The name of the form field (e.g., "Gender", "Blood Type").
            values (List[ValueData]): A list of possible values associated with this field.
                Defaults to an empty list.
        """
    name: str
    values: List[ValueData] = field(default_factory=lambda: [ ] )