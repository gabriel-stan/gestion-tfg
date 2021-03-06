from django.db import models
from authentication.models import Profesor, Alumno
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from eventos.models import Convocatoria
from notificaciones.services import email_asig_tfg
from authentication.models import Titulacion
import utils



class TfgManager(BaseUserManager):

    def create(self, titulo, **kwargs):
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
            else:
                try:
                    tutor = Profesor.objects.get(email=kwargs.get('tutor'))
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El tutor no existe')
                if not tutor.groups.filter(name='Profesores').exists():
                    raise NameError("Tutor ha de ser un profesor")

            # comprobando cotutor
            cotutor = None
            if not kwargs.get('cotutor') is None:
                try:
                    cotutor = Profesor.objects.get(email=kwargs.get('cotutor'))
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El cotutor no existe')
                if not cotutor.groups.filter(name='Profesores').exists():
                    raise NameError("Cotutor ha de ser un profesor")

            # comprobando titulacion
            if kwargs.get('titulacion') is None:
                raise NameError("Titulacion necesaria")
            else:
                try:
                    titulacion = Titulacion.objects.get(codigo=kwargs.get('titulacion'))
                except Titulacion.DoesNotExist:
                    return dict(status=False, message='la titulacion no existe')

            tfg = self.model(tipo=kwargs.get('tipo'), titulo=titulo,
                        n_alumnos=kwargs.get('n_alumnos'), descripcion=kwargs.get('descripcion'),
                        conocimientos_previos=kwargs.get('conocimientos_previos'),
                        hard_soft=kwargs.get('hard_soft'), tutor=tutor,
                        cotutor=cotutor, titulacion=titulacion)

            tfg.save()
            return dict(status=True, data=Tfg.objects.get(titulo=tfg.titulo))

        except NameError as e:
            return dict(status=False, message=e.message)

    def simular_create_tfg(self, titulo, **kwargs):
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
            else:
                try:
                    tutor = Profesor.objects.get(email=kwargs.get('tutor'))
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El tutor no existe')
                if not tutor.groups.filter(name='Profesores').exists():
                    raise NameError("Tutor ha de ser un profesor")

            # comprobando cotutor
            cotutor = None
            if not kwargs.get('cotutor') is None:
                try:
                    cotutor = Profesor.objects.get(email=kwargs.get('cotutor'))
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El cotutor no existe')
                if not cotutor.groups.filter(name='Profesores').exists():
                    raise NameError("Cotutor ha de ser un profesor")

            # comprobando titulacion
            if kwargs.get('titulacion') is None:
                raise NameError("Titulacion necesaria")
            else:
                try:
                    titulacion = Titulacion.objects.get(codigo=kwargs.get('titulacion'))
                except Titulacion.DoesNotExist:
                    return dict(status=False, message='la titulacion no existe')

            self.model(tipo=kwargs.get('tipo'), titulo=titulo, n_alumnos=kwargs.get('n_alumnos'),
                       descripcion=kwargs.get('descripcion'), conocimientos_previos=kwargs.get('conocimientos_previos'),
                       hard_soft=kwargs.get('hard_soft'), tutor=tutor, cotutor=cotutor, titulacion=titulacion)

            return True
        except NameError as e:
            return e.message

    def create_file(self, **kwargs):
        try:
            tutor = Profesor.objects.get(email=kwargs.get('tutor'))
            cotutor = Profesor.objects.get(email=kwargs.get('cotutor'))

            tfg = self.model(tipo=kwargs.get('tipo'), titulo=kwargs.get('titulo'),
                        n_alumnos=kwargs.get('n_alumnos'), descripcion=kwargs.get('descripcion'),
                        conocimientos_previos=kwargs.get('conocimientos_previos'),
                        hard_soft=kwargs.get('hard_soft'), tutor=tutor,
                        cotutor=cotutor)
            tfg.save()
            return dict(status=True, data=Tfg.objects.get(titulo=tfg.titulo))

        except NameError as e:
            return dict(status=False, message=e.message)


class Tfg(models.Model):
    tipo = models.CharField(max_length=100)
    titulo = models.TextField(max_length=250)
    n_alumnos = models.IntegerField()
    descripcion = models.TextField()
    conocimientos_previos = models.TextField(null=True)
    hard_soft = models.TextField(null=True)
    tutor = models.ForeignKey(Profesor, related_name='tutor', default=None)
    cotutor = models.ForeignKey(Profesor, related_name='cotutor', default=None, null=True)
    publicado = models.BooleanField(default=False)
    validado = models.BooleanField(default=False)
    asignado = models.BooleanField(default=False)
    titulacion = models.ForeignKey(Titulacion, related_name='titulacion', default=None)

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

    def to_dict(self, user):
        return dict(titulo=self.titulo, tipo=self.tipo, n_alumnos=self.n_alumnos,
                    descripcion=self.descripcion, conocimientos_previos=self.conocimientos_previos,
                    hard_soft=self.hard_soft, tutor=self.tutor.to_dict(user),
                    cotutor=self.cotutor.to_dict(user) if self.cotutor else None, publicado=self.publicado,
                    validado=self.validado, titulacion=self.titulacion.to_dict(), created_at=self.created_at,
                    updated_at=self.updated_at)


class Tfg_AsigManager(BaseUserManager):

    def create(self, tfg, alumno_1, alumno_2=None, alumno_3=None):
        alumno2_ok = False
        alumno3_ok = False
        try:
            # Compruebo lo minimo para asignar el tfg
            if not isinstance(tfg, Tfg) or not isinstance(alumno_1, Alumno) or not alumno_1.groups.filter(
                    name='Alumnos').exists():
                raise NameError("Error en los parametros de entrada")

            if utils.existe_tfg_asig(alumno_1):
                raise NameError("El alumno ya tiene un Tfg asignado")
            # Compruebo que no este ya asignado
            try:
                Tfg_Asig.objects.get(tfg=tfg)
                raise NameError("Tfg ya asignado")
            except Tfg_Asig.DoesNotExist:
                if not utils.comprueba_alumno(alumno_1) or utils.existe_tfg_asig(alumno_1):
                    raise NameError("Error en el primer alumno")

                if utils.comprueba_alumno(alumno_2) and not utils.existe_tfg_asig(alumno_2):
                    alumno2_ok = True
                if utils.comprueba_alumno(alumno_3) and not utils.existe_tfg_asig(alumno_3):
                    alumno3_ok = True

                # Si tiene 2 alumnos
                if alumno_2 and not alumno_3:
                    if not alumno2_ok:
                        raise NameError("Error en el segundo alumno")
                    else:
                        tfg_asig = self.model(tfg=tfg, alumno_1=alumno_1, alumno_2=alumno_2)
                # Si tiene 3 alumnos
                elif alumno_2 and alumno_3:
                    if not alumno2_ok or not alumno3_ok:
                        raise NameError("Error en el tercer alumno")
                    else:
                        tfg_asig = self.model(tfg=tfg, alumno_1=alumno_1, alumno_2=alumno_2, alumno_3=alumno_3)
                # Si tiene 1 alumno
                else:
                    tfg_asig = self.model(tfg=tfg, alumno_1=alumno_1, alumno_2=alumno_2, alumno_3=alumno_3)
                tfg_asig.save()
                tfg.asignado = True
                tfg.save()
                # email_asig_tfg(tfg.titulo, [alumno_1.email if alumno_1.email else '', alumno_2.email if (alumno_2 and alumno_2.email) else '',
                #                             alumno_3.email if (alumno_3 and alumno_3.email) else ''])
                return dict(status=True, data=Tfg_Asig.objects.get(tfg=tfg))

        except NameError as e:
            return dict(status=False, message=e.message)

    def simular_create_tfg_asig(self, tfg, alumno_1, alumno_2=None, alumno_3=None):
        alumno2_ok = False
        alumno3_ok = False
        try:
            # Compruebo lo minimo para asignar el tfg
            if not isinstance(tfg, Tfg):
                raise NameError("Error en los parametros de entrada")

            if not utils.is_email_alumno(alumno_1) and not utils.is_dni(alumno_1):
                raise NameError("Error en el primer alumno")

            if alumno_2 and not utils.is_email_alumno(alumno_2) and not utils.is_dni(alumno_2):
                raise NameError("Error en el segundo alumno")

            if alumno_3 and not utils.is_email_alumno(alumno_3) and not utils.is_dni(alumno_3):
                raise NameError("Error en el tercer alumno")

            if utils.existe_tfg_asig(alumno_1):
                raise NameError("el alumno %s ya tiene un tfg asignado" % alumno_1)
            # Compruebo que no este ya asignado
            try:
                Tfg_Asig.objects.get(tfg=tfg)
                raise NameError("Tfg ya asignado")
            except Tfg_Asig.DoesNotExist:
                if not utils.existe_tfg_asig(alumno_2):
                    alumno2_ok = True
                if not utils.existe_tfg_asig(alumno_3):
                    alumno3_ok = True

                # Si tiene 2 alumnos
                if alumno_2 and not alumno_3:
                    if not alumno2_ok:
                        raise NameError("Error en el segundo alumno")
                    else:
                        self.model(tfg=tfg, alumno_1=alumno_1, alumno_2=alumno_2)
                # Si tiene 3 alumnos
                elif alumno_2 and alumno_3:
                    if not alumno2_ok or not alumno3_ok:
                        raise NameError("Error en el tercer alumno")
                    else:
                        self.model(tfg=tfg, alumno_1=alumno_1, alumno_2=alumno_2, alumno_3=alumno_3)
                # Si tiene 1 alumno
                else:
                    self.model(tfg=tfg, alumno_1=alumno_1)
                return True
        except NameError as e:
            return e.message


class Tfg_Asig(models.Model):
    tfg = models.ForeignKey(Tfg, default=None)
    alumno_1 = models.ForeignKey(Alumno, related_name='alumno_1', default=None)
    alumno_2 = models.ForeignKey(Alumno, related_name='alumno_2', default=None, null=True)
    alumno_3 = models.ForeignKey(Alumno, related_name='alumno_3', default=None, null=True)
    convocatoria = models.ForeignKey(Convocatoria, related_name='convocatoria', default=None, null=True)
    fecha_conv = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Tfg_AsigManager()

    USERNAME_FIELD = 'tfg'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.tfg

    def get_alumno_1(self):
        return self.alumno_1

    def get_alumno_2(self):
        return self.alumno_2

    def get_alumno_3(self):
        return self.alumno_3

    def to_dict(self, user):
        return dict(id=self.id, tfg=self.tfg.to_dict(user), alumno_1=self.alumno_1.to_dict(user),
                    alumno_2=self.alumno_2.to_dict(user) if self.alumno_2 else None,
                    alumno_3=self.alumno_3.to_dict(user) if self.alumno_3 else None,
                    convocatoria=self.convocatoria.to_dict()if self.convocatoria else None,
                    fecha_conv=self.fecha_conv if self.fecha_conv else None,
                    created_at=self.created_at, updated_at=self.updated_at)
