 # -*- coding: utf-8 -*-

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.utils import timezone
from sysacad_api import SysacadSession
from sysacad_wrapper.settings import FR_BASE_URL

class SysacadBackend(object):
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
			if alumno.check_password(password, alumno.password):
				return alumno

	def get_user(self, user_id):
		try:
			Alumno.objects.get(pk=user_id)
		except Alumno.DoesNotExist:
			return None