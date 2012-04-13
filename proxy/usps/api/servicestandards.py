"""
Service standards API wrappers
"""
from usps.utils import dicttoxml, xmltodict
from usps.api.base import USPSService

try:
    from xml.etree import ElementTree as ET
except ImportError:
    from elementtree import ElementTree as ET
    
    


class ServiceStandards(USPSService):
    SERVICE_NAME = ''
    PARAMETERS = [
                  'OriginZip',
                  'DestinationZip'
                  ]
    
    
    def make_xml(self, data, user_id):
        """
        Transform the data provided to an XML fragment
        @param userid: the USPS API user id
        @param data: the data to serialize and send to USPS
        @return: an XML fragment representing data
        """
        for data_dict in data:
            data_xml = dicttoxml(data_dict, self.SERVICE_NAME+'Request', self.PARAMETERS)
            data_xml.attrib['USERID'] = user_id
        return data_xml
    
    def parse_xml(self, xml):
        """
        Parse the response from USPS into a dictionary
        @param xml: the xml to parse
        @return: a dictionary representing the XML response from USPS
        """
        return [xmltodict(xml),]
    

class PriorityMailServiceStandards(ServiceStandards):
    """
    Provides shipping time estimates for Priority mail shipping methods
    """
    SERVICE_NAME = 'PriorityMail'


class PackageServicesServiceStandards(ServiceStandards):
    """
    Provides shipping time estimates for Package Services (Parcel Post, Bound Printed Matter, Library Mail, and Media Mail)
    """
    SERVICE_NAME = 'StandardB'
    
    
class ExpressMailServiceCommitment(ServiceStandards):
    """
    Provides drop off locations and commitments for shipment on a given date
    """
    SERVICE_NAME = 'ExpressMailCommitment'
    PARAMETERS = [
                  'OriginZIP',
                  'DestinationZIP',
                  'Date'
                  ]

CLASSID_TO_SERVICE = {
                      'Priority': [0,1,12,16,17,18,19,22,28],
                      'Package': [4,5,6,7],
                      'Express': [2,3,13,23,25,27]
                      }
    
def get_service_standards(package_data, url, user_id):
    """
    Given a package class id return the appropriate service standards api class
    for calculating a domestic service standard or express mail commitment
    
    @param package_data: a dictionary containing OriginZip, DestinationZip, CLASSID, and optional Date keys
    @param: url a URL to send api calls to
    @param: user_id a valid USPS user id
    @return: a service standard estimate for the provided data as a string or False
    """
    classid = package_data.get('CLASSID', False)
    connection = False
    if classid in CLASSID_TO_SERVICE['Express']:
        data = {}
        data['OriginZIP'] = package_data.get('OriginZip')
        data['DestinationZIP'] = package_data.get('DestinationZip')
        data['Date'] = package_data.get('Date', "")
        
        connection = ExpressMailServiceCommitment(url, user_id)
        response = connection.execute([data])[0]   

        commitment = response.get('Commitment')
        if type(commitment).__name__ == 'list':
            delivery_time = commitment[0].get('CommitmentName', False)
        else:
            delivery_time = commitment.get('CommitmentName', False)
        
    else:    
        if classid in CLASSID_TO_SERVICE['Package']:
            connection = PackageServicesServiceStandards(url, user_id)
        elif classid in CLASSID_TO_SERVICE['Priority']:
            connection = PackageServicesServiceStandards(url, user_id)

        if connection:            
            package_data.pop('Date', None)
            response = connection.execute([package_data])[0]
            delivery_time = '%s Days' % response.get('Days')
        else:
            delivery_time = False
            
    return delivery_time
    
