from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from website.auth import AuthenticationForm
from django.contrib.auth.decorators import login_required
import website.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.dashboard'),
    url(r'^ajax/dashboard_data/$', 'website.views.dashboard_data'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'authentication_form': AuthenticationForm}),
    url(r'^ajustes-personales/$', login_required(website.views.AjustesPersonalesView.as_view())),
    url(r'^admin/', include(admin.site.urls)),
)
