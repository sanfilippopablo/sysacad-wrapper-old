from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from website.auth import AuthenticationForm
from django.contrib.auth.decorators import login_required
import website.views, website.ajax_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Auth views
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'authentication_form': AuthenticationForm}, name='login'),
    url(r'^admin/', include(admin.site.urls), name='admin'),

    # Normal views
    url(r'^$', 'website.views.dashboard', name='dashboard'),
    url(r'^ajustes-personales/$', login_required(website.views.AjustesPersonalesView.as_view()), name='ajustes-personales'),
    url(r'^materias/$', website.views.materias, name='materias'),

    # Ajax views
    url(r'^ajax/dashboard_data/$', website.ajax_views.dashboard_data, name='ajax-dashboard-data'), 
    url(r'^ajax/renew-sysacad-session/$', website.ajax_views.renew_sysacad_session, name='ajax-renew-sysacad-session'),
)