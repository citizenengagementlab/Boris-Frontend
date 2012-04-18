from django.conf.urls.defaults import *

urlpatterns = patterns('usps.views',
    (r'^zip_lookup$', 'zip_lookup'),
)