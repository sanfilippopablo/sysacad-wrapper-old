 # -*- coding: utf-8 -*-
from __future__ import division
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils import timezone
import pickle

materia_dificultad = (
	('e', 'Easy'),
	('m', 'Medium'),
	('h', 'Hard'),
)

class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    plan = models.CharField(max_length=10)
    anio = models.CharField(max_length=2)
    dificultad = models.CharField(max_length=2, choices=materia_dificultad, null=True)

    def __unicode__(self):
    	return self.nombre

class Carrera(models.Model):
	nombre = models.CharField(max_length=128)

	def __unicode__(self):
		return self.nombre

class EstadoMateria(models.Model):
	materia = models.ForeignKey(Materia)
	estado = models.CharField(max_length=32)
	aula = models.CharField(max_length=64, blank=True, null=True)
	nota = models.IntegerField(blank=True, null=True)
	tomo = models.IntegerField(blank=True, null=True)
	folio = models.IntegerField(blank=True, null=True)
	comision = models.CharField(max_length=24)

	def __unicode__(self):
		return u'%s: %s' % (self.materia.nombre, self.estado)

	class Meta:
		verbose_name = u'estado de materia'
		verbose_name_plural = u'estados de materia'

class AlumnoManager(BaseUserManager):

    def _create_user(self, fr, legajo, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(fr=fr, legajo=legajo, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        session = Session()
        session.save()
        user.session = session
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


class Session(models.Model):
	session = models.TextField(null=True)
	last_access = models.DateTimeField(default=timezone.now())

	def set_session(self, session):
		self.session = pickle.dumps(session)

	def get_session(self):
		return pickle.loads(self.session)

class Alumno(AbstractUser):

	fr = models.CharField(max_length=5)
	carrera = models.ForeignKey(Carrera, blank=True, null=True)
	legajo = models.CharField(max_length=30)
	last_activity = models.DateTimeField(default=timezone.now())
	session = models.ForeignKey(Session, null=True)
	materias = models.ManyToManyField(EstadoMateria, blank=True, null=True)

	objects = AlumnoManager()

	REQUIRED_FIELDS = ['fr', 'legajo', 'email']

	def is_ready_for_request(self):
		if (timezone.now() - self.last_activity) > timedelta(seconds=SESSION_DURATION):
			return False
		return True

	def actualizar_materias(self, materias_dict):
		for mat in materias_dict:
			# Actualizar la tabla materias (esto se hace la primera vez)

			# Ignorar año materias de ingreso.
			if int(mat['anio']) == 0:
				continue

			try:
				materia_obj = Materia.objects.get(nombre=mat['nombre'])
			except Materia.DoesNotExist:
				materia_obj = Materia.objects.create(
					nombre = mat['nombre'],
					plan = mat['plan'],
					anio = mat['anio']
				)

			# Actualizar materias de alumno.
			# Acá estoy seteando todo otra vez. Pero hay que verificar, no setear todo otra vez.
			# Así si detectamos un cambio mandamos la Notification.
			al_mat = self.materias.get_or_create(materia=materia_obj)[0]
			if mat['estado']['estado'] == 'aprobada':
				al_mat.estado = 'aprobada'
				al_mat.nota = mat['estado']['nota']
				al_mat.tomo = mat['estado']['tomo']
				al_mat.folio = mat['estado']['folio']
			elif mat['estado']['estado'] == 'cursa':
				al_mat.estado = 'cursa'
				al_mat.aula = mat['estado']['aula']
				al_mat.comision = mat['estado']['comision']
			elif mat['estado']['estado'] == 'regular':
				al_mat.estado = 'regular'
			al_mat.save()
		return self.materias

	def get_materia_percent(self, estado):
		return int(round((self.materias.filter(estado=estado).count() / self.materias.count()) * 100))

	def get_carrera_progress(self):
		a = self.get_materia_percent('aprobada')
		r = self.get_materia_percent('regular')
		c = self.get_materia_percent('cursa')
		return str(int(a + (r / 4) + (c / 8)))