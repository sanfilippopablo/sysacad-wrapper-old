from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from website.views import HomeView

urlpatterns = patterns('',
    # Examples:
     url(r'^$', HomeView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
)
