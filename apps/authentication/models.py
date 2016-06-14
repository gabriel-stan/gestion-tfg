import re
import utils
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
import signals


class AccountManager(BaseUserManager):

    def create_user(self, password=None, **kwargs):
        email = kwargs.get('email')
        dni = kwargs.get('dni')
        if not email and not dni:
            raise ValueError('Los usuarios deben tener un DNI o un email valido.')

        if email:
            email = self.normalize_email(email)

        account = self.model(
            email=email,
            dni=dni
        )

        account.set_password(password)
        account.save()

        return dict(status=True, data=account)

    def create_superuser(self, password, **kwargs):
        account = self.create_user(password, **kwargs)

        account['data'].is_admin = True
        account['data'].save()

        return account


class Usuario(AbstractBaseUser, PermissionsMixin):

    dni = models.CharField(default=None, unique=True, null=True, max_length=9)
    email = models.EmailField(default=None, unique=True, null=True)
    # username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    # tagline = models.CharField(max_length=140, blank=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([str(self.first_name), str(self.last_name)])

    def get_short_name(self):
        return self.first_name

    def get_email(self):
        return self.email


class Administrador(Usuario):
    pass


class AlumnoManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        try:
            if kwargs.get('email'):
                # exp reg para saber si el nick corresponde al correo de la ugr (@correo.ugr.es)
                if not re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$', kwargs.get('email')):
                    raise NameError("El email no es correcto o no pertenece a la UGR")

                res = Alumno.objects.filter(email=kwargs.get('email'))
                if res.count() != 0:
                    raise NameError("El alumno ya existe")
            if kwargs.get('dni'):
                # exp reg para saber si el nick corresponde al correo de la ugr (@correo.ugr.es)
                if not re.match(r'(\d{8})([-]?)([A-Z]{1})', kwargs.get('dni')):
                    raise NameError("Error en el DNI del alumno")

            if kwargs.get('first_name') and not utils.is_string(kwargs.get('first_name')):
                raise NameError("Nombre incorrecto")

            if kwargs.get('last_name') and not utils.is_string(kwargs.get('last_name')):
                raise NameError("Apellidos incorrectos")

            usuario = self.model.objects.create(email=kwargs.get('email'), dni=kwargs.get('dni'),
                                                first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'))

            grupo_alumnos = Grupos.objects.get(name='Alumnos')
            usuario.set_password(password)
            usuario.save()
            grupo_alumnos.user_set.add(usuario)
            return dict(status=True, data=usuario)

        except NameError as e:
            return dict(status=False, message=e.message)


class Alumno(Usuario):
    objects = AlumnoManager()


class Departamento(models.Model):
    nombre = models.CharField(default=None, unique=True, null=True, max_length=50)
    codigo = models.CharField(default=None, unique=True, null=True, max_length=10)

    USERNAME_FIELD = 'codigo'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.codigo


class ProfesorManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        try:
            if kwargs.get('email'):
                if not (kwargs.get('email') or not (re.match(r'^[a-z][_a-z0-9]+(@ugr\.es)$', kwargs.get('email')))):
                    raise NameError("El correo no es correcto")
                res = Profesor.objects.filter(email=kwargs.get('email'))
                if res.count() != 0:
                    raise NameError("El profesor ya existe")
            if kwargs.get('dni'):
                # exp reg para saber si el nick corresponde al correo de la ugr (@correo.ugr.es)
                if not re.match(r'(\d{8})([-]?)([A-Z]{1})', kwargs.get('dni')):
                    raise NameError("Error en el DNI del profesor")

            if not kwargs.get('first_name') or not utils.is_string(kwargs.get('first_name')):
                raise NameError("Error en el nombre del profesor")

            if not kwargs.get('last_name') or not utils.is_string(kwargs.get('last_name')):
                raise NameError("Error en los apellidos del profesor")

            if not kwargs.get('departamento') or not isinstance(kwargs.get('departamento'), Departamento):
                raise NameError("Error en el departamento")

            usuario = self.model.objects.create(email=kwargs.get('email'), dni=kwargs.get('dni'),
                                                first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'),
                                                departamento=kwargs.get('departamento'))

            grupo_profesores = Grupos.objects.get(name='Profesores')
            usuario.set_password(password)
            usuario.save()
            grupo_profesores.user_set.add(usuario)

            return dict(status=True, data=Profesor.objects.get(email=usuario.email))

        except NameError as e:
            return dict(status=False, message=e.message)


class Profesor(Usuario):

    departamento = models.ForeignKey(Departamento, related_name='departamento', default=None, null=True)
    objects = ProfesorManager()

    def get_departamento(self):
        return self.departamento


class Grupos(Group):
    code = models.IntegerField()

    class Meta:
        verbose_name_plural = "Grupos"
        ordering = ['code']
