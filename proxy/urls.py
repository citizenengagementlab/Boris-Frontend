from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('proxy.views',
    (r'^$', 'register'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^rtv/(?P<url>.*)$', 'rtv-proxy'),
    (r'^usps/',include('usps.urls'))
)