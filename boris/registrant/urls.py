from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
    (r'^map/$', 'map'),
    (r'^map2/$', 'map2'),
    (r'^start/$', 'start'),
    (r'^new/$', 'register'),
    (r'^submit/$', 'submit'),
    (r'^error/$', 'error'),
)
