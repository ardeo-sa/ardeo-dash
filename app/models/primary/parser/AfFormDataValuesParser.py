import xml.etree.ElementTree as ET
from typing import Dict

from app.models.primary.dataclass.AfFormDataValues import ValueData, FormValue


def parse_form_values(xml_str: str) -> Dict[str, FormValue]:
    root = ET.fromstring(xml_str)
    form_values_map = root.find("formValuesMap")
    values_dict = {}

    for entry in form_values_map.findall("entry"):
        key = entry.find("key").text
        value_elem = entry.find("value")
        name = value_elem.attrib.get("name", "")

        value_data_list = []
        for val_elem in value_elem.findall("values"):
            label_elem = val_elem.find("label")
            code_elem = val_elem.find("code")

            label = label_elem.text if label_elem is not None else ''
            code = code_elem.text if code_elem is not None else ''
            value_data_list.append(ValueData(label=label, code=code))

        values_dict[key] = FormValue(name=name, values=value_data_list)

    return values_dict