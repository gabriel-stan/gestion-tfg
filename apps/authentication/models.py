import re
import utils
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group


class AccountManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class Usuario(AbstractBaseUser):

    email = models.EmailField(unique=True)
    # username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    # tagline = models.CharField(max_length=140, blank=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
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


class Alumno(Usuario):

    def create_user(self, email, password=None, **kwargs):
        try:
            if not email:
                raise NameError("Error en el email del alumno")
            else:
                res = Alumno.objects.filter(email=kwargs.get('email'))
                if res.count() != 0:
                    raise NameError("El alumno ya existe")

            if not kwargs.get('first_name') or not utils.is_string(kwargs.get('last_name')):
                raise NameError("Nombre incorrecto")

            if not kwargs.get('last_name') or not utils.is_string(kwargs.get('last_name')):
                raise NameError("Apellidos incorrectos")

            # exp reg para saber si el nick corresponde al correo de la ugr (@correo.ugr.es)
            if not re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$', kwargs.get('email')):
                raise NameError("El email no es correcto")

            alumno = self.model(email=kwargs.get('email'), first_name=kwargs.get('first_name'),
                                last_name=kwargs.get('last_name'))

            grupo_alumnos = Group.objects.get(name='Alumnos')
            #alumno.set_password(password)
            alumno.save()
            grupo_alumnos.user_set.add(alumno)

            return dict(status=True, data=alumno)

        except NameError as e:
            return dict(status=False, message=e.message)


class Profesor(Usuario):
    departamento = models.CharField(max_length=100)

    def get_departamento(self):
        return self.departamento

    def create_user(self, email, password=None, **kwargs):
        try:
            if not email or not (re.match(r'^[a-z][_a-z0-9]+(@ugr\.es)$', email)):
                raise NameError("El correo no es correcto")
            else:
                res = Profesor.objects.filter(email=email)
                if res.count() != 0:
                    raise NameError("El profesor ya existe")

            if not kwargs.get('first_name') or not utils.is_string(kwargs.get('first_name')):
                raise NameError("Error en el nombre del profesor")

            if not kwargs.get('last_name') or not utils.is_string(kwargs.get('last_name')):
                raise NameError("Error en los apellidos del profesor")

            if not kwargs.get('departamento') or not utils.is_string(kwargs.get('departamento')):
                raise NameError("Error en el departamento")

            profesor = self.model(email=kwargs.get('email'), first_name=kwargs.get('first_name'),
                                last_name=kwargs.get('last_name'), departamento=kwargs.get('departamento'))

            grupo_profesores = Group.objects.get(name='Profesores')
            #profesor.set_password(password)
            profesor.save()
            grupo_profesores.user_set.add(profesor)

            return dict(status=True, data=Profesor.objects.get(username=profesor.username))

        except NameError as e:
            return dict(status=False, message=e.message)