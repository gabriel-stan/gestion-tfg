import re
import simplejson as json
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import Permission


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
    from models import Alumno, Profesor, Usuario
    resultado = []
    if isinstance(data, dict):
        data = [data]

    for s_data in data:
        resul = {}
        if user.is_admin:
            resul['dni'] = s_data['dni']
        resul['email'] = s_data['email']
        resul['first_name'] = s_data['first_name']
        resul['last_name'] = s_data['last_name']
        resul['created_at'] = s_data['created_at']
        resul['updated_at'] = s_data['updated_at']

        profesor = ''

        if s_data['dni'] is not None:
            if Alumno.objects.filter(dni=s_data['dni']).count() != 0:
                resul['clase'] = 'Alumno'
            elif Profesor.objects.filter(dni=s_data['dni']).count() != 0:
                resul['clase'] = 'Profesor'
                profesor = Profesor.objects.get(dni=s_data['dni'])
            # elif Usuario.objects.get(dni=s_data['dni']).is_admin:
            #     resul['clase'] = 'Administrador'
            else:
                resul['clase'] = 'Usuario'

        elif s_data['email'] is not None:
            if Alumno.objects.filter(email=s_data['email']).count() != 0:
                resul['clase'] = 'Alumno'
            elif Profesor.objects.filter(email=s_data['email']).count() != 0:
                resul['clase'] = 'Profesor'
                profesor = Profesor.objects.get(email=s_data['email'])
            # elif Usuario.objects.get(email=s_data['email']).is_admin:
            #     resul['clase'] = 'Administrador'
            else:
                resul['clase'] = 'Usuario'

        else:
            resul['clase'] = ''

        if resul['clase'] == 'Profesor':
            resul['departamento'] = profesor.departamento.codigo
        else:
            resul['departamento'] = ''

        resul['grupos'] = obtener_grupos(s_data)
        resul['is_admin'] = s_data['is_admin']
        resultado.append(resul)
    return resultado


def procesar_datos_departamento(data):
    # Importo aqui para evitar el cruce de imports
    from models import Profesor, Grupos
    group = Grupos.objects.get(name='Jefe de Departamento')
    users = group.user_set.all()
    resultado = []
    for s_data in data:
        departamento = {}
        departamento['codigo'] = s_data.codigo
        departamento['id'] = s_data.id
        departamento['nombre'] = s_data.nombre
        for s_users in users:
            if s_users.departamento.codigo == s_data.codigo:
                departamento['jefe_departamento'] = s_users
        resultado.append(departamento)
    return resultado


def obtener_grupos(data):
    grupos = []
    for grupo in data.get('groups') or []:
        grupos.append(grupo.get('name'))
    return grupos