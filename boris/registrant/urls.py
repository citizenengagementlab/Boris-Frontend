from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
    (r'^new/$', 'register'),
    (r'^submit/$', 'submit'),
    (r'^download/$', 'download'),
    (r'^finish/$', 'finish'),
)
