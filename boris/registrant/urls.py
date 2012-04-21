from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
    (r'^new/$', 'register'),
    (r'^save_registrant/$', 'save_registrant'),
    (r'^save_progress/$', 'save_progress'),
    (r'^submit/$', 'submit'),
    (r'^finish/$', 'finish'),
)
