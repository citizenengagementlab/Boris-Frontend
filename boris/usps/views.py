from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import render_to_response
from django.conf import settings
import json

from usps.errors import USPSXMLError
from urllib2 import URLError
from usps.api import USPS_CONNECTION_TEST, USPS_CONNECTION
from usps.api.addressinformation import CityStateLookup

def zip_lookup(request):
    USERID = settings.USPS_USERID
    connector = CityStateLookup(USPS_CONNECTION, USERID)
    
    zip5 = request.GET.get('zip')
    
    if len(zip5) > 5:
        #might be a zip9, try to parse zip5
        zip5 = zip5[:5]
    if zip5:
        try:
            response = connector.execute([{'Zip5':zip5}])[0]
            cleaned = {}
            cleaned['city'] = response['City'].lower().title()
            cleaned['state'] = response['State'].upper()
            cleaned['zip'] = response['Zip5']
            #print cleaned
        except USPSXMLError,e:
            return HttpResponseServerError('USPS Error: %s' % e)
        except URLError,e:
            return HttpResponseServerError(json.dumps({'error':'timeout'}),mimetype="application/json")
    else:
        return HttpResponseServerError('requires zip get parameter')
    
    return HttpResponse(json.dumps(cleaned),mimetype="application/json")