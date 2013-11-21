from django.db import models
from website.auth import Alumno, AccessCookie

class FacultadRegional(models.Model):
	codigo = models.CharField(max_length=5)
	nombre = models.CharField(max_length=30)
	base_url = models.URLField(max_length=256)

class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    plan = models.CharField(max_length=10)
    anio = models.CharField(max_length=2)

class Carrera(models.Model):
	nombre = models.CharField(max_length=128)

class EstadoMateria(models.Model):
	estado = models.CharField(max_length=32)
	lugar = models.CharField(max_length=64, blank=True, null=True)
	nota = models.IntegerField(blank=True, null=True)
	tomo = models.IntegerField(blank=True, null=True)
	folio = models.IntegerField(blank=True, null=True)