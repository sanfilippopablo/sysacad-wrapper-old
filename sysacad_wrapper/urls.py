from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from website.auth import AuthenticationForm
from django.contrib.auth.decorators import login_required
import website.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.dashboard', name='dashboard'),
    url(r'^ajax/dashboard_data/$', 'website.views.dashboard_data'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'authentication_form': AuthenticationForm}, name='login'),
    url(r'^ajustes-personales/$', login_required(website.views.AjustesPersonalesView.as_view()), name='ajustes-personales'),
    url(r'^ajax/renew-sysacad-session/$', website.views.renew_sysacad_session, name='ajax-renew-sysacad-session'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^materias/$', website.views.materias, name='materias'),
)
