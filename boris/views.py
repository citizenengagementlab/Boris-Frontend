from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.storage import staticfiles_storage

from os.path import join
import pygeoip
import urllib

from registrant.utils import removeNonAscii

@csrf_exempt
def frontpage(request):
    params = {}

    #geolocation didn't help, turn it off
    #lookup IP and redirect user to correct state
    #using free MaxMind GeoLiteCity db
    #geoip = pygeoip.GeoIP(join(settings.MEDIA_ROOT,'GeoLiteCity.dat'))
    #ip_addr = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR')
    #try:
    #    result = geoip.record_by_addr(ip_addr)
    #except pygeoip.GeoIPError:
    #    result = None
    #if result and result.has_key('region_name'):
    #    redirect_url = reverse('registrant.views.register')
    #    params['state'] = result['region_name']

    #now everybody redirects to first step
    redirect_url = reverse('registrant.views.map')

    #preserve  get parameters in redirect
    #to be backwards compatible with old rocky frontend
    for p in request.GET:
        params[p] = removeNonAscii(request.GET.get(p))
    if params.has_key('state'):
        #redirect to the form, not the map
        redirect_url = reverse('registrant.views.register')

    if params:
        redirect_url += "?"+urllib.urlencode(params)
    return redirect(redirect_url)

def static_redirect(request,path):
    redirect_url = staticfiles_storage.url(path)
    print redirect_url
    if request.GET:
        redirect_url += "?"+urllib.urlencode(request.GET)
    return redirect(redirect_url)

def rtv_iframe_test(request):
    layout = request.GET.get('layout')
    context = {'layout':layout}
    return render_to_response('rtv_iframe_test.html',context,
                context_instance=RequestContext(request))

def p3p_policy(request):
    return render_to_response('p3p.xml',{},
                context_instance=RequestContext(request))
