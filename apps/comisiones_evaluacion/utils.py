from django.db.models.fields.related import ManyToManyField
from authentication.models import Alumno, Profesor
from comisiones_evaluacion.models import Comision_Evaluacion, Tribunales
from eventos.models import Periodo
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
            data[f.name]['id'] = f.value_from_object(instance)

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
    elif is_string(usuario) and Profesor.objects.get(email=usuario):
        return True
    else:
        return False


def procesamiento(comision):
    resul = {}
    resul['presidente'] = unicode(comision.presidente)
    resul['titular_1'] = unicode(comision.presidente)
    resul['titular_2'] = unicode(comision.presidente)
    resul['sup_presidente'] = unicode(comision.presidente)
    resul['sup_titular_1'] = unicode(comision.sup_titular_1) if comision.sup_titular_1 else None
    resul['sup_titular_2'] = unicode(comision.sup_titular_2) if comision.sup_titular_2 else None

    return resul


def intercambiar_miembros(comision_1, comision_2, miembro_1, miembro_2):
    miembro_1_obj = getattr(comision_1, miembro_1)
    miembro_2_obj = getattr(comision_2, miembro_2)
    setattr(comision_1, miembro_1, miembro_2_obj)
    setattr(comision_2, miembro_2, miembro_1_obj)


def check_miembro_repetido(comision, miembro):
    if miembro in [comision.presidente.email, comision.vocal_1.email, comision.vocal_2.email, comision.suplente_1.email,
                   comision.suplente_2.email]:
        return False
    else:
        return True


def check_miembro(comision, miembro):
    comisiones = Comision_Evaluacion.objects.all()
    for i in comisiones:
        if i.id is not comision.id:
            if miembro == i.presidente:
                return 'presidente', i.id
            if miembro == i.vocal_1:
                return 'vocal_1', i.id
            if miembro == i.vocal_2:
                return 'vocal_2', i.id
            if miembro == i.suplente_1:
                return 'suplente_1', i.id
            if miembro == i.suplente_2:
                return 'suplente_2', i.id
    return False


def check_convocatoria(convocatoria, tipo):
    periodos = Periodo.objects.for_period()
    for periodo in periodos:
        if periodo.evento.convocatoria == convocatoria and periodo.evento.tipo == tipo:
            return True
    return False


def check_tfg_tribunal(tfg):
    if Tribunales.objects.filter(tfg=tfg).exists():
        return False
    else:
        return True

def procesar_datos_tribunales(user, data):
    # Importo aqui para evitar el cruce de imports
    from tfgs.models import Tfg_Asig
    if isinstance(data, dict):
        data = [data]
    for key, s_data in enumerate(data):
        data[key]['tfg'] = collections.OrderedDict(Tfg_Asig.objects.get(id=s_data['tfg']['id']).to_dict(user))
        # data[key]['comision'] = collections.OrderedDict(Comision_Evaluacion.objects.get(id=s_data['comision']).to_dict(user))
    return data


def procesar_datos_comisiones(user, data):
    # Importo aqui para evitar el cruce de imports
    from tfgs.models import Tfg_Asig
    from eventos.models import Convocatoria
    if isinstance(data, dict):
        data = [data]
    for key, s_data in enumerate(data):
        data[key]['presidente'] = collections.OrderedDict(Profesor.objects.get(id=s_data['presidente']['id']).to_dict(user))
        data[key]['vocal_1'] = collections.OrderedDict(Profesor.objects.get(id=s_data['vocal_1']['id']).to_dict(user))
        data[key]['vocal_2'] = collections.OrderedDict(Profesor.objects.get(id=s_data['vocal_2']['id']).to_dict(user))
        data[key]['suplente_1'] = collections.OrderedDict(Profesor.objects.get(id=s_data['suplente_1']['id']).to_dict(user))
        data[key]['suplente_2'] = collections.OrderedDict(Profesor.objects.get(id=s_data['suplente_2']['id']).to_dict(user))
        data[key]['convocatoria'] = collections.OrderedDict(Convocatoria.objects.get(id=s_data['convocatoria']['id']).to_dict())
    return data