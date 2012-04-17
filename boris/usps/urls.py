from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('usps.views',
    (r'^zip_lookup$', 'zip_lookup'),
)