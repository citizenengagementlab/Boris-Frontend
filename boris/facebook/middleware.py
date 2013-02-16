from django.conf import settings
from facebook.canvas import decode_signed_request
import logging

logger = logger = logging.getLogger(__name__)

#from http://djangosnippets.org/snippets/2272/

class FacebookCanvasMiddleware(object):
    def process_request(self, request):
        signed_request = request.REQUEST.get('signed_request', None)
        if signed_request:
            try:
                signed_request = decode_signed_request(settings.FACEBOOK_APP_SECRET, str(signed_request))
            except ValueError:
                #can't decode signed request
                signed_request = None
            request.csrf_processing_done = (signed_request != None)
            #stop csrf processing
            request.session['facebook_canvas'] = True
            #save to session

            if signed_request:
                #check against facebook partners list
                try:
                    fb_page_id = signed_request['page']['id']
                except KeyError,e:
                    logger.info("facebook app error",exc_info=True,
                        extra={'request':request})
                    return {}

                fb_partner_map = settings.FACEBOOK_PARTNERS_MAP

                if fb_page_id in fb_partner_map.keys():
                    request.session['facebook_partner_id'] = fb_partner_map[fb_page_id]
                else:
                    #rtv default
                    request.session['facebook_partner_id'] = 19093

                #set source, if not already set
                if not request.GET.get('source'):
                    request.session['facebook_source'] = "FBAPP"
