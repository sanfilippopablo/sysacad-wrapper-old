 # -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils import timezone

class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    plan = models.CharField(max_length=10)
    anio = models.CharField(max_length=2)

class Carrera(models.Model):
	nombre = models.CharField(max_length=128)

class EstadoMateria(models.Model):
	materia = models.ForeignKey(Materia)
	estado = models.CharField(max_length=32)
	lugar = models.CharField(max_length=64, blank=True, null=True)
	nota = models.IntegerField(blank=True, null=True)
	tomo = models.IntegerField(blank=True, null=True)
	folio = models.IntegerField(blank=True, null=True)

class AlumnoManager(BaseUserManager):

    def _create_user(self, fr, legajo, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(fr=fr, legajo=legajo, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        cookie = AccessCookie()
        cookie.save()
        user.cookies = cookie
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


class AccessCookie(models.Model):
	key = models.CharField(max_length=20, null=True)
	value = models.CharField(max_length=24, null=True)
	last_access = models.DateTimeField(default=timezone.now())

class Alumno(AbstractUser):

	fr = models.CharField(max_length=5)
	carrera = models.ForeignKey(Carrera, blank=True, null=True)
	legajo = models.CharField(max_length=30)
	last_activity = models.DateTimeField(default=timezone.now())
	cookies = models.ForeignKey(AccessCookie, null=True)
	materias = models.ManyToManyField(EstadoMateria, blank=True, null=True)

	objects = AlumnoManager()

	REQUIRED_FIELDS = ['fr', 'legajo', 'email']

	def is_ready_for_request(self):
		if (timezone.now() - self.last_activity) > timedelta(seconds=SESSION_DURATION):
			return False
		return True