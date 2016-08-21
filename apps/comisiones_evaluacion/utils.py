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


def check_miembro(comision, presidente):
    comisiones = Comision_Evaluacion.all()
    for i in comisiones:
        if presidente in (i.presidente, i.titular_1, i.titular_2, i.suplente_1, i.suplente_2) and \
                        i.id is not comision.id:
            return False
    if presidente.departamento == comision.titular_1.departamento or presidente.departamento == \
            comision.titular_2.departamento:
        return False
    return True


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