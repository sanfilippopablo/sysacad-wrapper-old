 # -*- coding: utf-8 -*-
from website.models import Alumno
from django.db import models
from django.utils import timezone
from sysacad_api import SysacadSession
from sysacad_wrapper.settings import FR, SESSION_DURATION
from django import forms
from django.contrib.auth import authenticate
from datetime import datetime, timedelta

class SysacadAuthBackend(object):
	def authenticate(self, fr=None, legajo=None, password=None):
		s = SysacadSession(FR[fr]['base_url'])
		try:
			s.login(legajo, password)
		except:
			return None
		try:
			alumno = Alumno.objects.get(fr=fr, legajo=legajo)
		except Alumno.DoesNotExist:
			alumno = Alumno.objects.create_user(fr, legajo)
			alumno.set_password(password)
			datos = s.datosAlumno()
			alumno.first_name = datos['nombre']
			alumno.last_name = datos['apellido']
			alumno.save()
		else:
			if not alumno.check_password(password):
				alumno.set_password(password)
		alumno.last_activity = timezone.now()
		alumno.cookies.last_access = timezone.now()
		alumno.cookies.key = s.cookies.keys()[0]
		alumno.cookies.value = s.cookies.values()[0]
		alumno.cookies.save()
		alumno.save()
		return alumno

	def get_user(self, user_id):
		try:
			return Alumno.objects.get(pk=user_id)
		except Alumno.DoesNotExist:
			return None

class AuthenticationForm(forms.Form):

	fr = forms.CharField(label="Facultad Regional", max_length=10)
	legajo = forms.CharField(label="Legajo", max_length=30)
	password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

	error_messages = {
		'invalid_login': "Información de login incorrecta."
	}

	def __init__(self, request, *args, **kwargs):
		self.user_cache = None
		super(AuthenticationForm, self).__init__(*args, **kwargs)

	def clean(self):
		fr = self.cleaned_data.get('fr')
		legajo = self.cleaned_data.get('legajo')
		password = self.cleaned_data.get('password')

		if fr and legajo and password:
			self.user_cache = authenticate(fr=fr,
										   legajo=legajo,
										   password=password)
			if self.user_cache is None:
				raise forms.ValidationError(self.error_messages['invalid_login'])

		return self.cleaned_data

	def get_user_id(self):
		if self.user_cache:
			return self.user_cache.id
		return None

	def get_user(self):
		return self.user_cache