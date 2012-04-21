from django.conf.urls.defaults import *

urlpatterns = patterns('proxy.views',
    (r'^(?P<url>.*)$', 'rtv_proxy_view'),
)