from django.db.models.fields.related import ManyToManyField
from authentication.models import Alumno, Profesor
from eventos.models import Periodo, Evento, Tipo_Evento
import simplejson as json
import re
import collections


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
def check_usuario(user, email):
    if user.email == email:
        return True
    elif user.is_admin:
        return True
    else:
        return False


def existe_tfg_asig(alumno):

    if alumno:
        if not isinstance(alumno, Alumno):
            alumno = Alumno.objects.get(email=alumno)
        from tfgs.models import Tfg_Asig
        alumno1 = Tfg_Asig.objects.filter(alumno_1=alumno)
        alumno2 = Tfg_Asig.objects.filter(alumno_2=alumno)
        alumno3 = Tfg_Asig.objects.filter(alumno_3=alumno)

        if alumno1.count() > 0 or alumno2.count() > 0 or alumno3.count() > 0:
            resul = True
        else:
            resul = False
    else:
        resul = False
    return resul


def comprueba_profesor(usuario):

    if isinstance(usuario, Profesor) and usuario.groups.filter(name='Profesores').exists():
        return True
    elif is_string(usuario) and Profesor.objects.get(email=usuario):
        return True
    else:
        return False


def comprueba_alumno(usuario):

    if isinstance(usuario, Alumno) and usuario.groups.filter(name='Alumnos').exists():
        return True
    else:
        return False


def check_convocatoria(convocatoria, tipo):
    periodos = Periodo.objects.for_period()
    for periodo in periodos:
        if periodo.evento.tipo.convocatoria == convocatoria and periodo.evento.tipo == tipo:
            return True
    return False


def is_email_alumno(alumno):
    try:
        if isinstance(alumno, Alumno):
            alumno = alumno.email
        if not re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$', alumno):
            return False
        else:
            return True
    except Exception:
            return False


def procesar_datos_tfgs_asig(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Tfg, Tfg_Asig
    if isinstance(data, dict):
        data = [data]

    for key, s_data in enumerate(data):

        if s_data['alumno_1'] is not None:
            data[key]['alumno_1'] = collections.OrderedDict(Alumno.objects.get(id=s_data['alumno_1']).to_dict())

        if s_data['alumno_2'] is not None:
            data[key]['alumno_2'] = collections.OrderedDict(Alumno.objects.get(id=s_data['alumno_2']).to_dict())
        else:
            data[key]['alumno_2'] = ''

        if s_data['alumno_3'] is not None:
            data[key]['alumno_3'] = collections.OrderedDict(Alumno.objects.get(id=s_data['alumno_3']).to_dict())
        else:
            data[key]['alumno_3'] = ''

        if s_data['tfg'] is not None:
            data[key]['tfg'] = collections.OrderedDict(Tfg.objects.get(id=s_data['tfg']).to_dict())

    return data


def procesar_datos_tfgs(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Titulacion
    if isinstance(data, dict):
        data = [data]

    for key, s_data in enumerate(data):
        data[key]['tutor'] = collections.OrderedDict(Profesor.objects.get(id=s_data['tutor']).to_dict())
        data[key]['titulacion'] = collections.OrderedDict(Titulacion.objects.get(id=s_data['titulacion']).to_dict())
        if s_data['cotutor'] is not None:
            data[key]['cotutor'] = collections.OrderedDict(Profesor.objects.get(id=s_data['cotutor']).to_dict())
        else:
            data[key]['cotutor'] = ''
    return data

