from django.conf import settings
from facebook.canvas import decode_signed_request

#from http://djangosnippets.org/snippets/2272/

class IgnoreFbCsrfMiddleware(object):
    def process_request(self, request):
        signed_request = request.REQUEST.get('signed_request', None)
        if signed_request:
            signed_request = decode_signed_request(signed_request, settings.FACEBOOK_APP_SECRET)
            request.csrf_processing_done = signed_request != None