from gestion_tfg.models import Tfg, Tfg_Asig
from django.contrib.auth.models import User


def existe_tfg_asig(alumno):

    if not isinstance(alumno, User):
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

    if isinstance(usuario, User) and usuario.groups.filter(name='Profesores').exists():
        return True
    else:
        return False

def comprueba_alumno(usuario):

    if isinstance(usuario, User) and usuario.groups.filter(name='Alumnos').exists():
        return True
    else:
        return False