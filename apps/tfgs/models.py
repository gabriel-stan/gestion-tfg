import utils
from django.db import models
from authentication.models import Profesor, Alumno
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group


class TfgManager(BaseUserManager):

    def create_tfg(self, titulo, **kwargs):
        try:
            # comprobando titulo vacio o Tfg con el mismo titulo
            if not titulo:
                raise NameError("Titulo necesario")
            else:
                res = Tfg.objects.filter(titulo=titulo)
                if res.count() != 0:
                    raise NameError("El TFG ya existe")

            # comprobando tipo no vacio
            if not kwargs.get('tipo'):
                raise NameError("Tipo de TFG necesario")

            # comprobando numero de alumnos
            if kwargs.get('n_alumnos') is None or not utils.is_int(kwargs.get('n_alumnos')) or int(kwargs.get('n_alumnos')) <= 0 \
                    or int(kwargs.get('n_alumnos')) > 3:
                raise NameError("Numero de alumnos incorrecto")

            # comprobando descripcion
            if not kwargs.get('descripcion'):
                raise NameError("Descripcion necesaria")

            # comprobando tutor
            if kwargs.get('tutor') is None:
                raise NameError("Tutor necesario")
            elif not kwargs.get('tutor').groups.filter(name='Profesores').exists():
                raise NameError("Tutor ha de ser un profesor")

            # comprobando cotutor
            if kwargs.get('cotutor') is None:
                if not kwargs.get('cotutor').groups.filter(name='Profesores').exists():
                    raise NameError("Cotutor ha de ser un profesor")

            tfg = self.model(tipo=kwargs.get('tipo'), titulo=kwargs.get('titulo'),
                        n_alumnos=kwargs.get('n_alumnos'), descripcion=kwargs.get('descripcion'),
                        conocimientos_previos=kwargs.get('conocimientos_previos'),
                        hard_soft=kwargs.get('hard_soft'), tutor=kwargs.get('tutor'),
                        cotutor=kwargs.get('cotutor'))

            tfg.save()
            return dict(status=True, data=Tfg.objects.get(titulo=tfg.titulo))

        except NameError as e:
            return dict(status=False, message=e.message)


class Tfg(models.Model):
    tipo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    n_alumnos = models.IntegerField()
    descripcion = models.TextField()
    conocimientos_previos = models.CharField(max_length=100, null=True)
    hard_soft = models.CharField(max_length=100, null=True)
    tutor = models.ForeignKey(Profesor, related_name='tutor',default=None)
    cotutor = models.ForeignKey(Profesor, related_name='cotutor', default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TfgManager()

    USERNAME_FIELD = 'titulo'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.titulo

    def get_tipo(self):
        return self.tipo

    def get_n_alumnos(self):
        return self.n_alumnos

    def get_descripcion(self):
        return self.descripcion

    def get_conocimientos_previos(self):
        return self.conocimientos_previos

    def get_hard_soft(self):
        return self.hard_soft

    def get_tutor(self):
        return self.tutor

    def get_cotutor(self):
        return self.cotutor


class Tfg_Asig(models.Model):
    tfg = models.ForeignKey(Tfg, default=None)
    alumno_1 = models.ForeignKey(Alumno, related_name='alumno_1',default=None)
    alumno_2 = models.ForeignKey(Alumno, related_name='alumno_2', default=None, null=True)
    alumno_3 = models.ForeignKey(Alumno, related_name='alumno_3', default=None, null=True)
