from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('boris.views',
    (r'^$', 'frontpage'),
    (r'^rtv_iframe_test/$', 'rtv_iframe_test'),
    (r'^w3c/p3p\.xml$', 'p3p_policy'),
)

urlpatterns += patterns('',
    (r'^registrants/', include('registrant.urls')),
    (r'^rtv/', include('proxy.urls')),
    (r'^usps/',include('ziplookup.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

#static file patterns to be compatible with old site
urlpatterns += patterns('boris.views',
    (r'^widget_loader\.js', 'static_redirect', {'path':'widgetloader/widget_loader.js'}),
    (r'^widget_loader\.css', 'static_redirect', {'path':'widgetloader/css/style.css'}),
)

admin.autodiscover()
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
   )
else:
   urlpatterns += patterns('boris.views',
       (r'^static/(?P<path>.*)$', 'static_redirect'),
       (r'^media/(?P<path>.*)$', 'static_redirect'),
   )