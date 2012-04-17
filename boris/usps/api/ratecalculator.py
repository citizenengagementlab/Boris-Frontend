"""
Rate Calculator classes
"""
from usps.api.base import USPSService

class DomesticRateCalculator(USPSService):
    """
    Calculator for domestic shipping rates
    """
    SERVICE_NAME = 'RateV3'
    CHILD_XML_NAME = 'Package'

    PARAMETERS = ['Service',
                  'FirstClassMailType',
                  'ZipOrigination',
                  'ZipDestination',
                  'Pounds',
                  'Ounces',
                  'Container',
                  'Size',
                  'Width',
                  'Length',
                  'Height',
                  'Girth',
                  'Machinable',
                  'ReturnLocations',
                  'ShipDate',
                  ]
    
    
class InternationalRateCalculator(USPSService):
    """
    Calculator for international shipping rates
    """
    SERVICE_NAME = 'IntlRate'
    CHILD_XML_NAME = 'Package'
    PARAMETERS = [
                  'Pounds',
                  'Ounces',
                  'Machinable',
                  'MailType',
                  'GXG',
                  'Length',
                  'Width',
                  'Height',
                  'POBoxFlag',
                  'GiftFlag',
                  'ValueOfContents',
                  'Country',
                  ]