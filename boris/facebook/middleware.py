from django.conf import settings
from facebook.canvas import decode_signed_request

#from http://djangosnippets.org/snippets/2272/

class FacebookCanvasMiddleware(object):
    def process_request(self, request):
        signed_request = request.REQUEST.get('signed_request', None)
        if signed_request:
            try:
                signed_request = decode_signed_request(settings.FACEBOOK_APP_SECRET, str(signed_request))
            except ValueError:
                #can't decode signed request
                pass
            request.csrf_processing_done = (signed_request != None)
            #stop csrf processing
            request.session['facebook_canvas'] = True
            #save to session
