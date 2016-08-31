import re
import simplejson as json
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import Permission
from django import forms
import collections
import requests


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


def enviar_email_reset_password(usuario):
    from views import ResetPasswordRequestView
    try:
        ResetPasswordRequestView().post(usuario)
    except:
        pass


def get_params(req):
    datos = {}
    if req.method == 'GET':
        for key, value in req.query_params.items():
            if key == 'content':
                return value
            elif key == 'campos':
                datos[key] = json.loads(value)
            else:
                datos[key] = value
    else:
        for key, value in req.data.items():
            if key == 'content':
                return value
            elif key == 'campos':
                datos[key] = json.loads(value)
            elif 'list' in key:
                datos[key] = json.loads(value)
            else:
                datos[key] = value
    return datos


def is_string(s):
    try:
        if isinstance(s, int) or isinstance(s, float):
            raise ValueError
        unicode(s)
        return True
    except ValueError:
        return False


def is_int(s):
    try:
        if isinstance(s, str) or isinstance(s, float):
            raise ValueError
        int(s)
        return True
    except ValueError:
        return False


def is_email(param):
    try:
        if not re.match(r'^[a-z][_a-z0-9]+(@(correo\.)?ugr\.es)$', param):
            return False
        else:
            return True
    except Exception:
            return False


def is_dni(param):
    try:
        if not re.match(r'(\d{8})([-]?)([A-Z]{1})', param):
            return False
        else:
            return True
    except Exception:
            return False


def to_dict(resul):
    instance = resul['data']
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)

    resul['data'] = data
    return resul


def is_email_alumno(alumno):
    from authentication.models import Alumno
    try:
        if isinstance(alumno, Alumno):
            alumno = alumno.email
        if not re.match(r'^[_a-z0-9]+(@correo\.ugr\.es)$', alumno):
            return False
        else:
            return True
    except Exception:
            return False


def is_email_profesor(profesor):
    from authentication.models import Profesor
    try:
        if isinstance(profesor, Profesor):
            profesor = profesor.email
        if not re.match(r'^[a-z][_a-z0-9]+(@ugr\.es)$', profesor):
            return False
        else:
            return True
    except Exception:
            return False


# Comprueba que un usuario va a modificar los datos de si mismo
def check_usuario(user, credential=None):
    if credential in [user.email, user.dni]:
        return True
    elif user.is_admin:
        return True
    else:
        return False


def permisos(usuario):
    permissions = Permission.objects.filter(group=usuario.groups.all()).values('codename')
    list_permissions = {}
    for permission in permissions:
        model, codename = permission['codename'].split('.')
        if list_permissions.get(model):
            list_permissions[model].append(codename)
        else:
            list_permissions[model] = [codename]
    return list_permissions


def grupos(grupos):
    list_grupos=[]
    for s_grupos in grupos:
        list_grupos.append({'codigo': s_grupos.code, 'nombre': s_grupos.name})
    return list_grupos


def procesar_datos_usuario(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Alumno, Profesor, Departamento
    if isinstance(data, dict):
        data = [data]

    for key, s_data in enumerate(data):
        profesor = ''

        if s_data['dni'] is not None:
            if Alumno.objects.filter(dni=s_data['dni']).count() != 0:
                data[key]['clase'] = 'Alumno'
            elif Profesor.objects.filter(dni=s_data['dni']).count() != 0:
                data[key]['clase'] = 'Profesor'
                profesor = Profesor.objects.get(dni=s_data['dni'])
            # elif Usuario.objects.get(dni=s_data['dni']).is_admin:
            #     resul['clase'] = 'Administrador'
            else:
                data[key]['clase'] = 'Usuario'

        elif s_data['email'] is not None:
            if Alumno.objects.filter(email=s_data['email']).count() != 0:
                data[key]['clase'] = 'Alumno'
            elif Profesor.objects.filter(email=s_data['email']).count() != 0:
                data[key]['clase'] = 'Profesor'
                profesor = Profesor.objects.get(email=s_data['email'])
            # elif Usuario.objects.get(email=s_data['email']).is_admin:
            #     resul['clase'] = 'Administrador'
            else:
                data[key]['clase'] = 'Usuario'

        else:
            data[key]['clase'] = ''

        if data[key]['clase'] == 'Profesor':
            data[key]['departamento'] = collections.OrderedDict(Departamento.objects.get(
                codigo=profesor.departamento.codigo).to_dict())
            data[key]['jefe_departamento'] = profesor.jefe_departamento

        data[key]['grupos'] = obtener_grupos(s_data)
        if not user.is_admin:
            data[key].pop('dni', None)

    return data


def procesar_datos_departamento(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Profesor, Grupos
    group = Grupos.objects.get(name='Jefe de Departamento')
    users = group.user_set.all()
    if isinstance(data, dict):
        data = [data]
    for key, s_data in enumerate(data):
        for s_users in users:
            if s_users.profesor.departamento.codigo == s_data['codigo']:
                data[key]['jefe_departamento'] = collections.OrderedDict(s_users.profesor.to_dict(user))
    return data


def obtener_grupos(data):
    grupos = []
    for grupo in data.get('groups') or []:
        grupos.append(grupo.get('name'))
    return grupos