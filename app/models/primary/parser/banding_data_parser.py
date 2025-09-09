"""
Module for parsing XML data into BandingData objects.

This module provides functionality to convert XML-formatted banding information into
a list of `BandingData` instances, which can be used for classification, scoring,
or visualization purposes.

Classes:
    BandingData: Data model representing a band with a value, message, and color.

Functions:
    parse_banding_data(xml_str): Parses an XML string into a list of BandingData objects.
"""

import xml.etree.ElementTree as ET
from app.models.primary.dataclass.banding_data import BandingData


def parse_banding_data(xml_str):
    """
     Parses an XML string containing BandingData elements into a list of BandingData objects.

     Args:
         xml_str (str): XML string containing one or more <BandingData> elements.

     Returns:
         List[BandingData]: A list of BandingData instances parsed from the XML.
     """
    banding_data_list = []
    if not xml_str:
        return banding_data_list

    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        print(f"XML parsing failed: {e}")
        return banding_data_list

    for bd_elem in root.findall('BandingData'):
        try:
            bd = BandingData(
                lower_band=float(bd_elem.findtext('lower_band', default='0')),
                higher_band=float(bd_elem.findtext('higher_band', default='0')),
                assign_value=float(bd_elem.findtext('assign_value', default='0')),
                message=bd_elem.findtext('message', default=''),
                assign_color=bd_elem.findtext('assign_color', default='')
            )
            banding_data_list.append(bd)
        except (AttributeError, ValueError) as e:
            print(f"Error parsing BandingData element: {e}")

    return banding_data_list
