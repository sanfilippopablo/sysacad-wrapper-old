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

@login_required
def materias(request):
	materias = request.user.materias.all().select_related('materia').order_by('materia__anio', 'materia__nombre')
	return render_to_response('materias.html', RequestContext(request, locals()))