from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import render_to_response
from django.conf import settings
import json

from usps.errors import USPSXMLError
from usps.api import USPS_CONNECTION_TEST, USPS_CONNECTION
from usps.api.addressinformation import CityStateLookup

def zip_lookup(request):
    USERID = settings.USPS_USERID
    connector = CityStateLookup(USPS_CONNECTION, USERID)
    
    zip5 = request.GET.get('zip')
    if zip5:
        try:
            response = connector.execute([{'Zip5':zip5}])[0]
            cleaned = {}
            cleaned['city'] = response['City'].lower().title()
            cleaned['state'] = response['State'].upper()
            cleaned['zip'] = response['Zip5']
            print cleaned
        except USPSXMLError,e:
            return HttpResponseServerError('USPS Error: %s' % e)
    else:
        return HttpResponseServerError('requires zip get parameter')
    
    return HttpResponse(json.dumps(cleaned),mimetype="application/json")