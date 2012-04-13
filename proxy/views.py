import httplib2
from urllib import urlencode
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.conf import settings
PROXY_FORMAT = u"https://%s/%s" % (settings.PROXY_DOMAIN, u"%s")

def proxy(request, url):
    conn = httplib2.Http()
    # optionally provide authentication for server
    if settings.PROXY_CREDENTIALS:
        conn.add_credentials(settings.PROXY_CREDENTIALS['user'],
                             settings.PROXY_CREDENTIALS['password'])
                             
    print "PROXY",request.method,
    if request.method == "GET":
        print request.GET
        url_ending = "%s?%s" % (url, urlencode(request.GET))
        url = PROXY_FORMAT % url_ending
        resp, content = conn.request(url, request.method)
        return HttpResponse(content)
    elif request.method == "POST":
        print request.POST
        url = PROXY_FORMAT % url
        data = request.POST
        resp, content = conn.request(url, request.method, data)
        print "POST DATA",request.POST
        print "POST QUERY",data
        print "PROXY RESPONSE",content
        return HttpResponse(content)

def register(request):
    return render_to_response('form.html')