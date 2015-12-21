from django.db import models
from django.contrib.auth.models import Group, User, AbstractUser


class Alumno(AbstractUser):
    pass

class Profesor(Alumno):
    departamento = models.CharField(max_length=100)


class Tfg(models.Model):
    tipo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    n_alumnos = models.IntegerField()
    descripcion = models.TextField()
    conocimientos_previos = models.CharField(max_length=100)
    hard_soft = models.CharField(max_length=100)
    tutor = models.ForeignKey(Profesor, related_name='tutor',default=None)
    cotutor = models.ForeignKey(Profesor, related_name='cotutor', default=None)

class Tfg_Asig(models.Model):
    tfg = models.ForeignKey(Tfg, default=None)
    alumno_1 = models.ForeignKey(Alumno, related_name='alumno_1',default=None)
    alumno_2 = models.ForeignKey(Alumno, related_name='alumno_2', default=None, null=True)
    alumno_3 = models.ForeignKey(Alumno, related_name='alumno_3', default=None, null=True)

class Evaluacion_Tfg_Tutor(models.Model):
    tfg = models.ForeignKey(Tfg_Asig, default=None)
    tutor = models.ForeignKey(Profesor, related_name='tutor_tfg',default=None)
    departamento = models.CharField(max_length=100)
    fecha = models.DateField()
    calificacion = models.FloatField()
    sub_cal_1 = models.FloatField()
    sub_cal_2 = models.FloatField()
    sub_cal_3 = models.FloatField()
    sub_cal_4 = models.FloatField()
    sub_cal_5 = models.FloatField()
    sub_cal_6 = models.FloatField()
    sub_cal_7 = models.FloatField()
    sub_cal_8 = models.FloatField()
    observaciones = models.CharField(max_length=500, null=True)

class Comision_Evaluacion(models.Model):
    presidente = models.ForeignKey(Profesor, related_name='presidente', default=None)
    titular_1 = models.ForeignKey(Profesor, related_name='titular_1', default=None)
    titular_2 = models.ForeignKey(Profesor, related_name='titular_2', default=None, null=True)
    sup_presidente = models.ForeignKey(Profesor, related_name='sup_presidente', default=None)
    sup_titular_1 = models.ForeignKey(Profesor, related_name='sup_titular_1', default=None)
    sup_titular_2 = models.ForeignKey(Profesor, related_name='sup_titular_2', default=None, null=True)

class Tribunales(models.Model):
    tfg = models.ForeignKey(Tfg_Asig, default=None)
    comision = models.ForeignKey(Comision_Evaluacion, default=None)
    fecha = models.DateField()
    hora = models.DateTimeField()
    observaciones = models.CharField(max_length=500, null=True)

