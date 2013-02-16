from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache
from django.utils.http import urlquote_plus

import urllib2
import urllib
import json
import logging

logger = logging.getLogger(__name__)

PROXY_FORMAT = u"https://%s/%s" % (settings.PROXY_DOMAIN, u"%s")

def rtv_proxy_view(request,url):
    #wrapper for direct django view
    if request.method == "GET":
        response = rtv_proxy("GET",request.GET,url)
    elif request.method == "POST":
        response = rtv_proxy("POST",request.GET,url)
    elif request.method == "HEAD":
        exists = url_exists(PROXY_FORMAT % url)
        response = {'exists':exists,
            'error':not exists,
        }
        if exists:
            response['status'] = 200
        else:
            response['status'] = 404
    try:
        if response.has_key('error'):
            status = response['status']
        else:
            status = 200
    except UnboundLocalError:
        response = {'error':'unknown rtv proxy error'}
        status = 404
    return HttpResponse(json.dumps(response),mimetype="application/json",status=status)

def rtv_proxy(method, values, url):
    if settings.DEBUG: print "PROXY",method,
    if method == "GET":
        if settings.DEBUG: print values
        data = urllib.urlencode(values)
        url_ending = "%s?%s" % (url, data)
        url = PROXY_FORMAT % url_ending
    elif method == "POST":
        if settings.DEBUG: print values
        url = PROXY_FORMAT % url
        if 'registrations.json' in url:
            #don't use urllib.urlencode to encode data dictionary,
            #that munges the brackets, quote_plus the values and do &-join manually
            data = []
            for (k,v) in values.items():
                v_s = unicode(v).strip() #strip spaces, because rocky doesn't like them
                data.append('registration[%s]=%s' % (k,urlquote_plus(v_s)))
            data = "&".join(data)
        else:
            data = urllib.urlencode(values)
        if settings.DEBUG: print "POST QUERY",data
    
    if hasattr(settings,'PROXY_CREDENTIALS'):
        #setup a password manager to handle the authentication
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
        url_opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(url_opener)
        password_manager.add_password(None, url, #none means don't specify realm
                                      settings.PROXY_CREDENTIALS['user'],
                                      settings.PROXY_CREDENTIALS['password'])
    try:
        if method == "GET":
            response = urllib2.urlopen(url)
        elif method == "POST":
            response = urllib2.urlopen(url,data)
    except urllib2.HTTPError,e:
        error_message = e.read()
        logger.error('rocky api error: %s' % e.code,exc_info=True,extra={'error_message':error_message})
        try:
            error_dict = {'error':json.loads(error_message)}
        except ValueError:
            error_dict = {'error':error_message}
        error_dict['status'] = e.code
        return error_dict
        
    content = response.read()
    return json.loads(content)

def rtv_proxy_cached(method, values, url):
    #cached proxy, should probably only be used for getting state requirements
    cache_key = "%s:%s:%s" % (method,url, ".".join(values.values()))
    if cache.get(cache_key):
        if settings.DEBUG: print "cache.get", cache_key
        return cache.get(cache_key)
    else:
        response = rtv_proxy(method,values,url)
        cache.set(cache_key,response,3600)
        if settings.DEBUG: print "cache.set", cache_key
        return response


def url_exists(url):
    #use HEAD method to get only response code, not full contents
    class HeadRequest(urllib2.Request):
        def get_method(self):
            return "HEAD"

    try:
        response = urllib2.urlopen(HeadRequest(url))
        return (response.code == 200)
    except urllib2.HTTPError:
        return False
    except Exception,e:
        if settings.DEBUG: print e
        return False

def partner_proxy(method,url,values):
    #values should be a dictionary at this point
    if settings.DEBUG: print "PARTNER PROXY",method

    if method == "POST":
        data = urllib.urlencode(values)
        try:
            response = urllib2.urlopen(url,data)
        except urllib2.HTTPError,e:
            error_dict = {'error':json.loads(e.read())}
            error_dict['status'] = e.code
            return error_dict

        if settings.DEBUG: print "PARTNER PROXY DATA",data

        content = response.read()
        return json.loads(content)