from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('boris.views',
    (r'^$', 'frontpage'),
    (r'^rtv_iframe_test/$', 'rtv_iframe_test'),
)

urlpatterns += patterns('',
    (r'^registrants/', include('registrant.urls')),
    (r'^rtv/', include('proxy.urls')),
    (r'^usps/',include('usps.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    )