from django.conf.urls.defaults import *

urlpatterns = patterns('ziplookup.views',
    (r'^zip_lookup/{0,1}$', 'zip_lookup'),
)