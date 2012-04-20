from django.conf.urls.defaults import *

urlpatterns = patterns('usps.views',
    (r'^zip_lookup/{0,1}$', 'zip_lookup'),
)