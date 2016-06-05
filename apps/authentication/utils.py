import re
import simplejson as json
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import Permission

def get_params(req):

    datos = {}
    if req.method == 'GET':
        for key, value in req.query_params.items():
            if key == 'campos':
                datos[key] = json.loads(value)
            else:
                datos[key] = value
    else:
        for key, value in req.data.items():
            if key == 'campos':
                datos[key] = json.loads(value)
            else:
                datos[key] = value
    return datos


def is_string(s):
    try:
        if isinstance(s, int) or isinstance(s, float):
            raise ValueError
        str(s)
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
        if not re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$', param):
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