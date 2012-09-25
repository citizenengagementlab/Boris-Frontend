from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import render_to_response
from django.conf import settings
import json

from ziplookup.models import ZipCode

def zip_lookup(request):
    
    zipcode = request.GET.get('zip')

    if len(zipcode) > 5:
        if '-' in zipcode:
            zip5,plus4 = zipcode.split('-')
        else:
            zip5 = zipcode[:5]
    else:
        zip5 = zipcode

    if zip5:
        try:
            place = ZipCode.objects.get(zipcode=zip5)
            cleaned = {}
            cleaned['city'] = place.city.lower().title()
            cleaned['state'] = place.state
            cleaned['zip'] = place.zipcode
            #print cleaned
        except ZipCode.DoesNotExist:
            #print e
            return HttpResponseServerError(json.dumps({'error':'unknown zipcode'}),mimetype="application/json")
    else:
        return HttpResponseServerError('requires zip get parameter')
    return HttpResponse(json.dumps(cleaned),mimetype="application/json")