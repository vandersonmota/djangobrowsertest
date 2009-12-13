from django.conf.urls.defaults import *

# from django.contrib import admin
# admin.autodiscover()

from testapp.views import hello_world

urlpatterns = patterns('',
      (r'^foo/$', hello_world),
    # (r'^admin/', include(admin.site.urls)),
)
