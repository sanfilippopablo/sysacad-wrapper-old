# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from website.auth import SysacadSession
from django.contrib.auth.decorators import login_required
from sysacad_wrapper.settings import FR
from django.utils import timezone
from datetime import timedelta, datetime
import json
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from website import forms as website_forms
from django.core.urlresolvers import reverse_lazy
from jsonview.decorators import json_view
from crispy_forms.utils import render_crispy_form
from django.views.generic.list import ListView

@json_view
@login_required
def dashboard_data(request):
	valid_session = (timezone.now() - request.user.session.last_access) < timedelta(seconds=200)
	if valid_session:
		sysacad = SysacadSession(alumno=request.user)
	else:
		return {'state': 'password_required'}

	materias_dict = sysacad.estado_academico_data()['materias']
	sysacad.close()
	materias = request.user.actualizar_materias(materias_dict).filter(estado='cursa')
	materias = request.user.materias.filter(estado='cursa')
	aprobadas_percent = request.user.get_materia_percent('aprobada')
	regularizadas_percent = request.user.get_materia_percent('regular')
	cursa_percent = request.user.get_materia_percent('cursa')
	carrera_progress = request.user.get_carrera_progress()
	context = {
		'materias': materias,
		'aprobadas_percent': aprobadas_percent,
		'regularizadas_percent': regularizadas_percent,
		'cursa_percent': cursa_percent,
		'carrera_progress': carrera_progress,
	}
	return {
		'state': 'OK',
		'html': render_to_string('dashboard_data.html', context)
	}

@json_view
def renew_sysacad_session(request):
	form = website_forms.RenewSysacadSessionForm(user=request.user, data=request.POST)
	if form.is_valid():
		return {'valid': True}
	else:
		form_html = render_crispy_form(form)
    	return {'valid': False, 'form_html': form_html}