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
        #str(s)
        if isinstance(s, basestring):
            return True
        else:
            raise ValueError
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


def is_bool(s):
    try:
        bool(s)
        return True
    except ValueError:
        return False


def to_bool(s):
    if not isinstance(s, bool):
        if s in ['true', '1', 't', 'y', 'yes', 'True', 'TRUE']:
            return True
        elif s in ['false', '0', 'f', 'n', 'no', 'False', 'FALSE']:
            return False
        else:
            raise NameError('Error en los parametros de entrada')
    else:
        return s


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
            try:
                alumno = Alumno.objects.get(email=alumno)
            except Alumno.DoesNotExist:
                raise NameError('No existe el alumno')
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
    try:
        if isinstance(usuario, Profesor) and usuario.groups.filter(name='Profesores').exists():
            return True
        elif is_string(usuario) and Profesor.objects.get(email=usuario):
            return True
        else:
            return False
    except Profesor.DoesNotExist:
        return False


def comprueba_alumno(usuario):

    if isinstance(usuario, Alumno) and usuario.groups.filter(name='Alumnos').exists():
        return True
    else:
        return False


def check_convocatoria(convocatoria, tipo):
    periodos = Periodo.objects.for_period()
    for periodo in periodos:
        if periodo.evento.convocatoria == convocatoria:
            return True
    return False


def check_tfg(user, tfg):
    from models import Tfg
    if Tfg.objects.filter(titulo=tfg, tutor=user).exists():
        return True
    else:
        return False


def is_email_alumno(alumno):
    try:
        if isinstance(alumno, Alumno):
            alumno = alumno.email
        if not re.match(r'^[_a-z0-9]+(@correo\.ugr\.es)$', alumno):
            return False
        else:
            return True
    except Exception:
            return False


def is_dni(alumno):
    try:
        if isinstance(alumno, Alumno):
            alumno = alumno.dni
        if not re.match(r' (([X-Z]{1})([-]?)(\d{7})([-]?)([A-Z]{1}))|((\d{8})([-]?)([A-Z]{1}))', alumno):
            return False
        else:
            return True
    except Exception:
            return False


def procesar_datos_tfgs_asig(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Tfg, Tfg_Asig, Convocatoria
    if isinstance(data, dict):
        data = [data]

    for key, s_data in enumerate(data):

        if s_data['alumno_1'] is not None:
            try:
                data[key]['alumno_1'] = collections.OrderedDict(Alumno.objects.get(id=s_data['alumno_1']).to_dict(user))
            except Alumno.DoesNotExist:
                data[key]['alumno_1'] = None
        if s_data['alumno_2'] is not None:
            try:
                data[key]['alumno_2'] = collections.OrderedDict(Alumno.objects.get(id=s_data['alumno_2']).to_dict(user))
            except Alumno.DoesNotExist:
                data[key]['alumno_2'] = None
        else:
            data[key]['alumno_2'] = ''

        if s_data['alumno_3'] is not None:
            try:
                data[key]['alumno_3'] = collections.OrderedDict(Alumno.objects.get(id=s_data['alumno_3']).to_dict(user))
            except Alumno.DoesNotExist:
                data[key]['alumno_3'] = None
        else:
            data[key]['alumno_3'] = ''

        if s_data['tfg'] is not None:
            try:
                data[key]['tfg'] = collections.OrderedDict(Tfg.objects.get(id=s_data['tfg']).to_dict(user))
            except Tfg.DoesNotExist:
                data[key]['tfg'] = None

        if s_data['convocatoria'] is not None:
            try:
                data[key]['convocatoria'] = collections.OrderedDict(Convocatoria.objects.get(id=s_data['convocatoria']).to_dict())
            except Convocatoria.DoesNotExist:
                data[key]['convocatoria'] = None

    return data


def procesar_datos_tfgs(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Titulacion
    if isinstance(data, dict):
        data = [data]

    for key, s_data in enumerate(data):
        try:
            data[key]['tutor'] = collections.OrderedDict(Profesor.objects.get(id=s_data['tutor']).to_dict(user))
        except Profesor.DoesNotExist:
            data[key]['tutor'] = None
        try:
            data[key]['titulacion'] = collections.OrderedDict(Titulacion.objects.get(id=s_data['titulacion']).to_dict())
        except Titulacion.DoesNotExist:
            data[key]['titulacion'] = None
        if s_data['cotutor'] is not None:
            try:
                data[key]['cotutor'] = collections.OrderedDict(Profesor.objects.get(id=s_data['cotutor']).to_dict(user))
            except Profesor.DoesNotExist:
                data[key]['cotutor'] = None
        else:
            data[key]['cotutor'] = ''
    return data


def procesar_params_tfg(user, data):
    # Importo aqui para evitar el cruce de imports
    from models import Titulacion
    for key, s_data in data.items():
        if key in ['tutor', 'cotutor']:
            try:
                data[key] = Profesor.objects.get(email=s_data)
            except Profesor.DoesNotExist:
                data[key] = None
        elif key == 'titulacion':
            try:
                data[key] = Titulacion.objects.get(codigo=s_data)
            except Profesor.Titulacion:
                data[key] = None
        elif key in ['publicado', 'asignado', 'validado'] and is_bool(s_data):
            data[key] = to_bool(s_data)
        elif key == 'n_alumnos' and is_int(s_data):
            data[key] = int(s_data)
    return _params_perfil(user, data)


def _params_perfil(user, data):
    if not getattr(user, 'is_admin', False) and not comprueba_profesor(getattr(user, 'email', '')):
        #data['asignado'] = False
        data['publicado'] = True
        data['validado'] = True
    return data


def get_or_create_alumno(email):
    if not Alumno.objects.filter(email=email if email else None).exists():
        Alumno.objects.create_user(email=email)
    try:
        return Alumno.objects.get(email=email)
    except Alumno.DoesNotExist:
        raise NameError('Error en el alumno %s' % email)