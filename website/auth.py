from django import models

class SysacadAuthBackend(object):
	def authenticate(self, fr=None, legajo=None, password=None):
		# Aca se hace lo que escribi en el CUU.
		pass

	def get_user(self, user_id):
		pass

class SysacadAlumnoManager(models.BaseUserManager):
	def create_user(self, fr, legajo, password=None):
		pass

	def create_superuser(self, fr, legajo, password):
		pass

frs = (
	('frro', 'Rosario'),
	('frre', 'Resistencia'),
)

class Alumno(models.Model):
	fr = models.CharField(max_length=10, choices=frs)
	legajo = models.CharField(max_length=30)
	password = models.CharField(max_length=100)