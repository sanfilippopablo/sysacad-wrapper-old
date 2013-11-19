 # -*- coding: utf-8 -*-

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone
from sysacad_api import SysacadSession
from sysacad_wrapper.settings import BASE_URL
class SysacadAuthBackend(object):
	def authenticate(self, fr=None, legajo=None, password=None):
		s = SysacadSession(fr, legajo, password)
		s.login()
		print s
		try:
			alumno = Alumno.objects.get(fr=fr, legajo=legajo)
		except Alumno.DoesNotExist:
			return Alumno.objects.create_user(fr=fr, legajo=legajo, password=password)
		else:
			if check_password(password, alumno.password):
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

class Alumno(AbstractUser):

	fr = models.CharField(max_length=10, choices=frs)
	legajo = models.CharField(max_length=30	)

	REQUIRED_FIELDS = ['fr', 'legajo', 'email']