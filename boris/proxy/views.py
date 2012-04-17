import urllib2,urllib,json
from django.http import HttpResponse

from django.conf import settings
PROXY_FORMAT = u"https://%s/%s" % (settings.PROXY_DOMAIN, u"%s")

def rtv_proxy(request, url):
    if settings.DEBUG: print "PROXY",request.method,
    if request.method == "GET":
        if settings.DEBUG: print request.GET
        url_ending = "%s?%s" % (url, urllib.urlencode(request.GET))
        url = PROXY_FORMAT % url_ending
    elif request.method == "POST":
        if settings.DEBUG: print request.POST
        url = PROXY_FORMAT % url
        #don't use urllib.urlencode to encode data dictionary,
        #that munges the brackets, do &-join manually and quote_plus the values
        data = []
        for (k,v) in request.POST.items():
            data.append('%s=%s' % (k,urllib.quote_plus(v)))
        data = "&".join(data)
        if settings.DEBUG: print "POST QUERY",data
    
    if settings.PROXY_CREDENTIALS:
        #setup a password manager to handle the authentication
        password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
        url_opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(url_opener)
        password_manager.add_password(None, url, #none means don't specify realm
                                      settings.PROXY_CREDENTIALS['user'],
                                      settings.PROXY_CREDENTIALS['password'])
    try:
        if request.method == "GET":
            response = urllib2.urlopen(url)
        elif request.method == "POST":
            response = urllib2.urlopen(url,data)
    except urllib2.HTTPError,e:
        return HttpResponse(e.read(),status=e.code)
        
    content = response.read()
    return HttpResponse(content,mimetype="application/json")