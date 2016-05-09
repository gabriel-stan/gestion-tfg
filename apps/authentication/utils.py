from django.db.models.fields.related import ManyToManyField
import simplejson as json
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
def check_usuario(user, email=None):
    if user.email == email:
        return True
    elif user.is_admin:
        return True
    else:
        return False


def permisos(usuario):
    permissions = Permission.objects.filter(group=usuario.groups.all()).values('codename')
    list_permissions = []
    for permission in permissions:
        model, codename = permission['codename'].split('.')
        list_permissions.append({model: codename})
    return list_permissions