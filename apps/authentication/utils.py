from django.db.models.fields.related import ManyToManyField

from model.models import Tfg_Asig, Profesor, Alumno
import simplejson as json


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
