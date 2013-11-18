from django import models
from sysacad_api import SysacadSession

class SysacadAuthBackend(object):
	def authenticate(self, fr=None, legajo=None, password=None):
		s = SysacadSession(fr, legajo, password)
		try:
			s.login()
		except:
			return None
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

class AlumnoManager(models.BaseUserManager):

	# TODO: Ir fijandome en el django sc los metodos de BaseUserManager que
	# no sirve e ir redefiniéndolos.

	def create_user(self, fr, legajo, password=None):
		pass

	def create_superuser(self, fr, legajo, password):
		pass

frs = (
	('frro', 'Rosario'),
	('frre', 'Resistencia'),
)

class Alumno(AbstractBaseUser):

	# TODO: Ir fijandome en el django sc los metodos de AbstractBaseUser que
	# no sirve e ir redefiniéndolos.

	fr = models.CharField(max_length=10, choices=frs)
	legajo = models.CharField(max_length=30)
	password = models.CharField(max_length=128)

	objects = AlumnoManager()