from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
    (r'^map/$', 'map'),
    (r'^new/$', 'register'),
    (r'^new/(?P<state_abbr>[a-zA-Z]{2})/$', 'direct_submit'),
    (r'^submit/$', 'submit'),
    (r'^error/$', 'error'),
)
