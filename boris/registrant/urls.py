from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
    (r'^map/$', 'map'),
    (r'^new/$', 'register'),
    (r'^new/wa(?i)/$', 'wa_direct'),
    (r'^submit/$', 'submit'),
    (r'^error/$', 'error'),
)
