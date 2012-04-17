from django.conf.urls.defaults import *

urlpatterns = patterns('boris.views',
    (r'^(?P<url>.*)$', 'rtv_proxy'),
)