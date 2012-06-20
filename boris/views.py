from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.core.urlresolvers import reverse
from django.conf import settings

from os.path import join
import pygeoip

def frontpage(request):
    #lookup IP and redirect user to correct state
    #using free MaxMind GeoLiteCity db
    geoip = pygeoip.GeoIP(join(settings.STATIC_ROOT,'GeoLiteCity.dat'))
    ip_addr = request.META['REMOTE_ADDR']
    if settings.DEBUG and ip_addr == "127.0.0.1":
        ip_addr = "75.101.48.104" #test with known CA IP
    result = geoip.record_by_addr(ip_addr)
    if result:
        params = "?state="+result['region_name']
        #params += "&zip="+result['postal_code']
        #zip probably not accurate enough to depend on free db
        return redirect(reverse('registrant.views.register')+params)
    else:
        #should redirect to map view
        #tmp, redirect to registration page w/o params
        return redirect(reverse('registrant.views.register'))

def rtv_iframe_test(request):
    layout = request.GET.get('layout')
    context = {'layout':layout}
    return render_to_response('rtv_iframe_test.html',context,
                context_instance=RequestContext(request))
                
def mockup(request):
    return render_to_response('rtv_iframe_mockup.html',{},
                context_instance=RequestContext(request))