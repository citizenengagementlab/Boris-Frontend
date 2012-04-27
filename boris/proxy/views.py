import urllib2,urllib,json
from django.http import HttpResponse

from django.conf import settings
PROXY_FORMAT = u"https://%s/%s" % (settings.PROXY_DOMAIN, u"%s")

def rtv_proxy_view(request,url):
    #wrapper for direct django view
    if request.method == "GET":
        response = rtv_proxy("GET",request.GET,url)
    elif request.method == "POST":
        response = rtv_proxy("POST",request.GET,url)
    if response.has_key('error'):
        status = response['status']
    else:
        status = 200
    return HttpResponse(json.dumps(response),mimetype="application/json",status=status)

def rtv_proxy(method, values, url):
    if settings.DEBUG: print "PROXY",method,
    if method == "GET":
        if settings.DEBUG: print values
        url_ending = "%s?%s" % (url, urllib.urlencode(values))
        url = PROXY_FORMAT % url_ending
    elif method == "POST":
        if settings.DEBUG: print values
        url = PROXY_FORMAT % url
        if 'registrations.json' in url:
            #don't use urllib.urlencode to encode data dictionary,
            #that munges the brackets, do &-join manually and quote_plus the values
            data = []
            for (k,v) in values.items():
                data.append('registration[%s]=%s' % (k,urllib.quote_plus(v)))
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
        error_dict = {'error':json.loads(e.read())}
        error_dict['status'] = e.code
        return error_dict
        
    content = response.read()
    return json.loads(content)