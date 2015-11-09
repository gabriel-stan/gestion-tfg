from gestion_tfg.models import Tfg, Tfg_Asig
from django.contrib.auth.models import User
from gestion_tfg.servicios.utils import *

def insert_tfg(tfg):

    # comprobando titulo vacio o Tfg con el mismo titulo
    if not tfg.titulo:
        return False
    else:
        res = Tfg.objects.filter(titulo=tfg.titulo)
        if res.count() != 0:
            return False

    # comprobando tipo no vacio
    if not tfg.tipo:
        return False

    # comprobando numero de alumnos
    if (tfg.n_alumnos is None) or (tfg.n_alumnos <= 0) or (tfg.n_alumnos > 3):
        return False

    #comprobando descripcion
    if not tfg.descripcion:
        return False

    #comprobando conocimientos previos
    if not tfg.conocimientos_previos:
        return False

    #comprobando requisitos HW SW
    if not tfg.hard_soft:
        return False

    #comprobando tutor
    if (not hasattr(tfg,'tutor')):
        return False

    #comprobando cotutor
    if (not hasattr(tfg,'cotutor')):
        return False

    tfg.save()
    return True

def update_tfg(tfg, campos):

    #comprobando titulo
    if 'titulo' in campos.keys():
        if campos['titulo'] == '' or not isinstance(campos['titulo'], str):
            return False
        else:
            tfg.titulo = campos['titulo']

    #comprobando tipo
    if 'tipo' in campos.keys():
        if campos['tipo'] == '' or not isinstance(campos['tipo'], str):
            return False
        else:
            tfg.tipo = campos['tipo']

    #comprobando n_alumnos
    if 'n_alumnos' in campos.keys():
        if (campos['n_alumnos'] <= 0) or (campos['n_alumnos'] > 3) or not(isinstance(campos['n_alumnos'], int)):
            return False
        else:
            tfg.n_alumnos = campos['n_alumnos']

    #comprobando descripcion
    if 'descripcion' in campos.keys():
        if campos['descripcion'] == '' or not isinstance(campos['descripcion'], str):
            return False
        else:
            tfg.descripcion = campos['descripcion']

    #comprobando conocimientos_previos
    if 'conocimientos_previos' in campos.keys():
        if campos['conocimientos_previos'] == '' or not isinstance(campos['conocimientos_previos'], str):
            return False
        else:
            tfg.conocimientos_previos = campos['conocimientos_previos']

    #comprobando hard_soft
    if 'hard_soft' in campos.keys():
        if campos['hard_soft'] == '' or not isinstance(campos['hard_soft'], str):
            return False
        else:
            tfg.hard_soft = campos['hard_soft']

    #comprobando tutor
    if 'tutor' in campos.keys():
        #NOTA: Cuando este el modelo de profesores, hay que ver que el tutor sea un profesor
        if not isinstance(campos['tutor'], User) or not campos['tutor'].groups.filter(name='Profesores').exists():
            return False
        else:
            tfg.tutor = campos['tutor']

    #comprobando cotutor
    if 'cotutor' in campos.keys():
        #NOTA: Cuando este el modelo de profesores, hay que ver que el tutor sea un profesor
        if not isinstance(campos['cotutor'], User) or not campos['cotutor'].groups.filter(name='Profesores').exists():
            return False
        else:
            tfg.tutor = campos['cotutor']

    tfg.save()

    return True

def delete_tfg(tfg):

    tfg.delete()

    try:
        Tfg.objects.get(titulo=tfg)
        return True
    except Tfg.DoesNotExist:
        return False

def asignar_tfg(tfg, alumno1, alumno2=None, alumno3=None):

    alumno2_ok = False
    alumno3_ok = False

    #Compruebo lo minimo para asignar el tfg
    if not isinstance(tfg, Tfg) or not isinstance(alumno1, User) or existe_tfg_asig(alumno1):
        return False

    #Compruebo que no este ya asignado
    try:
        Tfg_Asig.objects.get(tfg=tfg)
        return False
    except Tfg_Asig.DoesNotExist:
        if isinstance(alumno2, User) and not existe_tfg_asig(alumno2):
            alumno2_ok = True
        if isinstance(alumno3, User) and not existe_tfg_asig(alumno3):
            alumno3_ok = True

        #Si tiene 2 alumnos
        if alumno2 != None and alumno3 == None:
            if not alumno2_ok:
                return False
            else:
                tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1, alumno_2=alumno2)
                tfg_asig.save()
                return True
        #Si tiene 3 alumnos
        elif alumno2 != None and alumno3 != None:
            if not alumno2_ok or not alumno3_ok:
                return False
            else:
                tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1, alumno_2=alumno2, alumno_3=alumno3)
                tfg_asig.save()
                return True
        #Si tiene 1 alumno
        else:
            tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1)
            tfg_asig.save()
            return True