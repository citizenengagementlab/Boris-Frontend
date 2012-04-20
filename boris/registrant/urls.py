from django.conf.urls.defaults import *

urlpatterns = patterns('registrant.views',
    (r'^new/$', 'register'),
    (r'^submit/$', 'submit'),
    (r'^save_registrant/$', 'save_registrant'),
    (r'^save_progress/$', 'save_progress'),
    (r'^download/$', 'download'),
    (r'^finish/$', 'finish'),
)
