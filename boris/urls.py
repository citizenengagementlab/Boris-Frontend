from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('boris.views',
    (r'^$', 'frontpage'),
    (r'^registrants/new/$', 'register'),
    (r'^registrants/finish/$', 'finish'),
)

urlpatterns += patterns(
    (r'^rtv/(?P<url>.*)$', include('proxy.urls')),
    (r'^usps/',include('usps.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns(
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    )