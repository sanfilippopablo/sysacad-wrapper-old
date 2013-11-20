 # -*- coding: utf-8 -*-

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone
from sysacad_api import SysacadSession
from sysacad_wrapper.settings import FR_BASE_URL
from django import forms
from django.contrib.auth import authenticate

class SysacadAuthBackend(object):
	def authenticate(self, fr=None, legajo=None, password=None):
		s = SysacadSession(FR_BASE_URL[fr])
		try:
			s.login(legajo, password)
		except:
			return None
		try:
			alumno = Alumno.objects.get(fr=fr, legajo=legajo)
		except Alumno.DoesNotExist:
			alumno = Alumno.objects.create_user(fr, legajo)
			alumno.set_password(password)
			alumno.save()
			return alumno
		else:
			if not alumno.check_password(password):
				alumno.set_password(password)
			return alumno

	def get_user(self, user_id):
		try:
			Alumno.objects.get(pk=user_id)
		except Alumno.DoesNotExist:
			return None

frs = (
	('frro', 'Rosario'),
	('frre', 'Resistencia'),
)

class AlumnoManager(BaseUserManager):

    def _create_user(self, fr, legajo, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(fr=fr, legajo=legajo, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.username = user.fr + user.legajo
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, fr, legajo, email=None, password=None, **extra_fields):
        return self._create_user(fr, legajo, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, fr, legajo, email, password, **extra_fields):
        return self._create_user(fr, legajo, email, password, True, True,
                                 **extra_fields)

class Alumno(AbstractUser):

	fr = models.CharField(max_length=10, choices=frs)
	legajo = models.CharField(max_length=30)

	objects = AlumnoManager()

	REQUIRED_FIELDS = ['fr', 'legajo', 'email']

class AuthenticationForm(forms.Form):

	fr = forms.CharField(label="Facultad Regional", max_length=10)
	legajo = forms.CharField(label="Legajo", max_length=30)
	password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

	error_messages = {
		'invalid_login': "Información de login incorrecta."
	}

	def __init__(self, *args, **kwargs):
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