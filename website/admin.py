from django.contrib import admin
from website.models import Alumno, Session, Materia, EstadoMateria

# Register your models here.
admin.site.register(Alumno)
admin.site.register(Session)
admin.site.register(Materia)
admin.site.register(EstadoMateria)