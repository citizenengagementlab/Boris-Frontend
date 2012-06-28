from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
	(r'^map/$', 'map'),
    (r'^new/$', 'register'),
    (r'^submit/$', 'submit'),
    (r'^finish/$', 'finish'),
)
