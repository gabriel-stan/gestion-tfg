from django.db.models.fields.related import ManyToManyField
from authentication.models import Alumno, Profesor, Usuario
import simplejson as json
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

    if not isinstance(alumno, Alumno):
        return False
    else:
        from tfgs.models import Tfg_Asig
        alumno1 = Tfg_Asig.objects.filter(alumno_1=alumno)
        alumno2 = Tfg_Asig.objects.filter(alumno_2=alumno)
        alumno3 = Tfg_Asig.objects.filter(alumno_3=alumno)

        if alumno1.count() > 0 or alumno2.count() > 0 or alumno3.count() > 0:
            return True
        else:
            return False


def comprueba_profesor(usuario):

    if isinstance(usuario, Profesor) and usuario.groups.filter(name='Profesores').exists():
        return True
    else:
        return False


def comprueba_alumno(usuario):

    if isinstance(usuario, Alumno) and usuario.groups.filter(name='Alumnos').exists():
        return True
    else:
        return False


def procesar_datos_eventos(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Tipo_Evento, SubTipo_Evento, Periodo
    if isinstance(data, dict):
        data = [data]

    for key, s_data in enumerate(data):
        data[key]['autor'] = collections.OrderedDict(Usuario.objects.get(id=s_data['autor']).to_dict(user))
        data[key]['convocatoria'] = collections.OrderedDict(Tipo_Evento.objects.get(id=s_data['convocatoria']).to_dict())
        if s_data['tipo'] is not None:
            data[key]['tipo'] = collections.OrderedDict(SubTipo_Evento.objects.get(id=s_data['tipo']).to_dict())
        else:
            data[key]['tipo'] = ''
        try:
            periodo = Periodo.objects.get(evento=s_data['id'])
            data[key]['desde'] = periodo.start
            data[key]['hasta'] = periodo.end
        except Periodo.DoesNotExist:
            pass
    return data
