from django.db import models
from django.contrib.auth.models import Group, User


class Tfg(models.Model):
    tipo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    n_alumnos = models.IntegerField()
    descripcion = models.TextField()
    conocimientos_previos = models.CharField(max_length=100)
    hard_soft = models.CharField(max_length=100)
    tutor = models.ForeignKey(User, related_name='tutor',default=None)
    cotutor = models.ForeignKey(User, related_name='cotutor', default=None)

class Tfg_Asig(models.Model):
    titulo = models.ForeignKey(Tfg, default=None)
    alumno_1 = models.ForeignKey(User, related_name='alumno_1',default=None)
    alumno_2 = models.ForeignKey(User, related_name='alumno_2', default=None)
    alumno_3 = models.ForeignKey(User, related_name='alumno_3', default=None)