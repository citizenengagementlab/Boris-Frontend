"""
Track and Confirm class
"""
from usps.api.base import USPSService

try:
    from xml.etree import ElementTree as ET
except ImportError:
    from elementtree import ElementTree as ET

class TrackConfirm(USPSService):
    """
    Calculator for domestic shipping rates
    """
    SERVICE_NAME = 'Track'
    CHILD_XML_NAME = 'TrackID'
    API = 'TrackV2'
    
    def make_xml(self, data, user_id):
          
        root = ET.Element(self.SERVICE_NAME+'Request')
        root.attrib['USERID'] = user_id
        
        for data_dict in data:
            track_id = data_dict.get('ID', False)
            if track_id:
                data_xml = ET.Element('TrackID')
                data_xml.attrib['ID'] = str(track_id)
                root.append(data_xml) 
                 
        return root
    
    