from django.db.models.fields.related import ManyToManyField
import simplejson as json

from old.model import Tfg_Asig, Profesor, Alumno

def existe_tfg_asig(alumno):

    if not isinstance(alumno, Alumno):
        return False
    else:
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


def get_params(req):

    datos = {}
    if req.method == 'POST':
        for key, value in req.POST.items():
            if key == 'campos':
                datos[key] = json.loads(value)
            elif key == 'tutor' or key == 'cotutor':
                datos[key] = Profesor.objects.get(username=str(value))
            else:
                datos[key] = value
    else:
        for key, value in req.query_params.items():
            if key == 'campos':
                datos[key] = json.loads(value)
            elif key == 'tutor' or key == 'cotutor':
                datos[key] = Profesor.objects.get(username=str(value))
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
