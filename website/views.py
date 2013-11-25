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

@login_required
def dashboard(request):
	materias = request.user.materias.filter(estado='cursa')
	if materias.count() == 0:
		return render_to_response('dashboard.html', RequestContext(request, {'estado': 'new_user'}))
	aprobadas_percent = request.user.get_materia_percent('aprobada')
	regularizadas_percent = request.user.get_materia_percent('regular')
	cursa_percent = request.user.get_materia_percent('cursa')
	carrera_progress = request.user.get_carrera_progress()
	return render_to_response('dashboard.html', RequestContext(request, locals()))

@login_required
def dashboard_data(request):
	valid_cookie = (timezone.now() - request.user.cookies.last_access) < timedelta(seconds=200)
	if valid_cookie:
		s = SysacadSession(base_url=FR[request.user.fr]['base_url'], alumno=request.user)
	else:
		if request.POST.get('password'):
			s = SysacadSession(FR[request.user.fr]['base_url'])
			s.login(request.user.legajo, request.POST.get('password'))
		else:
			return HttpResponse(json.dumps({'state': 'password_required', 'html': render_to_string('password_required_modal.html')}), content_type="application/json")

	materias_dict = s.allDataFromEstadoAcademico()['materias']
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
	data = {
		'state': 'OK',
		'html': render_to_string('dashboard_data.html', context)
	}
	return HttpResponse(json.dumps(data), content_type="application/json")

class AjustesPersonalesView(FormView):
	template_name = 'ajustes-personales.html'
	form_class = website_forms.AjustesPersonalesForm
	success_url = reverse_lazy('ajustes-personales')

	def get_initial(self):
		initial = {'email': self.request.user.email}
		return initial

	def get_form_kwargs(self):
		kwargs = super(AjustesPersonalesView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		form.save()
		return super(AjustesPersonalesView, self).form_valid(form)