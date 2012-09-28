from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': 'map/'}),
)

urlpatterns += patterns('registrant.views',
    (r'^map/$', 'map'),
    (r'^new/$', 'register'),
    (r'^submit/$', 'submit'),
    (r'^new/(?P<state_abbr>[a-zA-Z]{2})/$', 'register_direct'),
    (r'^submit/(?P<state_abbr>[a-zA-Z]{2})/$', 'submit_direct'),
    (r'^share/$', 'share'),
    (r'^error/$', 'error'),
)
