import xml.etree.ElementTree as ET

from app.models.primary.dataclass.BandingData import BandingData


def parse_banding_data(xml_str):
    banding_data_list = []
    if not xml_str:
        return banding_data_list

    root = ET.fromstring(xml_str)
    for bd_elem in root.findall('BandingData'):
        try:
            bd = BandingData(
                lowerBand=float(bd_elem.findtext('lowerBand', default='0')),
                higherBand=float(bd_elem.findtext('higherBand', default='0')),
                assignValue=float(bd_elem.findtext('assignValue', default='0')),
                message=bd_elem.findtext('message', default=''),
                assignColor=bd_elem.findtext('assignColor', default='')
            )
            banding_data_list.append(bd)
        except Exception as e:
            print(f"Error parsing BandingData element: {e}")

    return banding_data_list
