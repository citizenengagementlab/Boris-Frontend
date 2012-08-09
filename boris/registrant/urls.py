from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
    (r'^map/$', 'map'),
    (r'^start/$', 'start'),
    (r'^new/$', 'register'),
    (r'^submit/$', 'submit'),
    (r'^error/$', 'error'),
)
