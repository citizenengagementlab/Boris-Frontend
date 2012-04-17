"""
Global errors module for USPS app 
"""
from usps.utils import xmltodict

class USPSXMLError(Exception):
    def __init__(self, element):
        self.info = xmltodict(element)
        super(USPSXMLError, self).__init__(self.info['Description'])