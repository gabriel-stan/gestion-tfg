from gestion_tfg.models import Comision_Evaluacion
from gestion_tfg.servicios.utils import *
import re

def insert_alumno(alumno):
    try:
        if not alumno.username:
            raise
        else:
            res = Alumno.objects.filter(username=alumno.username)
            if res.count() != 0:
                raise

        if not alumno.first_name or not isinstance(alumno.first_name, str):
            raise

        if not alumno.last_name or not isinstance(alumno.last_name, str):
            raise

        #exp reg para saber si el nick corresponde al correo de la ugr (@correo.ugr.es)
        if (re.match((r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$'), alumno.username)) == None:
            raise

        return Alumno.objects.create_user(username=alumno.username, first_name= alumno.first_name,last_name= alumno.last_name)

    except NameError:
        print 'error de valor'
        return False
    except:
        return False

def update_alumno(alumno, campos):
    try:
        # comprobando username
        if 'username' in campos.keys():
            res = Alumno.objects.filter(username=campos['username'])
            if res.count() == 0:
                if (re.match((r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$'), campos['username'])) == None:
                    raise
                else:
                    alumno.username = campos['username']
            else:
                raise

        # comprobando nombre
        if 'first_name' in campos.keys():
            if campos['first_name'] == '' or not isinstance(campos['first_name'], str):
                raise
            else:
                alumno.first_name = campos['first_name']

        # comprobando apellidos
        if 'last_name' in campos.keys():
            if campos['last_name'] == '' or not isinstance(campos['last_name'], str):
                raise
            else:
                alumno.last_name = campos['last_name']

        alumno.save()

        resul = Alumno.objects.get(username=alumno.username)
        return resul

    except NameError:
        print 'error de valor'
        return False
    except:
        return False

def delete_alumno(alumno):

    try:
        Alumno.objects.get(username=alumno.username).delete()
        return True
    except Alumno.DoesNotExist:
        return 'No existe'

def insert_profesor(profesor):

    try:
        if not profesor.username:
            raise
        else:
            res = Profesor.objects.filter(username=profesor.username)
            if res.count() != 0:
                raise

        if not profesor.first_name or not isinstance(profesor.first_name, str):
            raise

        if not profesor.last_name or not isinstance(profesor.last_name, str):
            raise

        if not profesor.departamento or not isinstance(profesor.departamento, str):
            raise

        #exp reg para saber si el nick corresponde al correo de la ugr (@correo.ugr.es)
        if (re.match((r'^[a-z][_a-z0-9]+(@ugr\.es)$'), profesor.username)) == None:
            raise

        return Profesor.objects.create_user(username=profesor.username, first_name= profesor.first_name,
                                        last_name= profesor.last_name, departamento=profesor.departamento)

    except NameError:
        print 'error de valor'
        return False
    except:
        return False

def update_profesor(profesor, campos):
    try:
        # comprobando username
        if 'username' in campos.keys():
            res = Profesor.objects.filter(username=campos['username'])
            if res.count() == 0:
                if (re.match((r'^[a-z][_a-z0-9]+(@ugr\.es)$'), campos['username'])) == None:
                    raise
                else:
                    profesor.username = campos['username']
            else:
                raise

        # comprobando nombre
        if 'first_name' in campos.keys():
            if campos['first_name'] == '' or not isinstance(campos['first_name'], str):
                raise
            else:
                profesor.first_name = campos['first_name']

        # comprobando apellidos
        if 'last_name' in campos.keys():
            if campos['last_name'] == '' or not isinstance(campos['last_name'], str):
                raise
            else:
                profesor.last_name = campos['last_name']

        # comprobando departamento
        if 'departamento' in campos.keys():
            if campos['departamento'] == '' or not isinstance(campos['departamento'], str):
                raise
            else:
                profesor.departamento = campos['departamento']

        profesor.save()

        resul = Profesor.objects.get(username=profesor.username)
        return resul

    except NameError:
        print 'error de valor'
        return False
    except:
        return False

def delete_profesor(profesor):

    try:
        Profesor.objects.get(username=profesor.username).delete()
        return True
    except Profesor.DoesNotExist:
        return 'No existe'

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

    # comprobando descripcion
    if not tfg.descripcion:
        return False

    # comprobando conocimientos previos
    if not tfg.conocimientos_previos:
        return False

    # comprobando requisitos HW SW
    if not tfg.hard_soft:
        return False

    # comprobando tutor
    if not hasattr(tfg, 'tutor'):
        return False
    elif not tfg.tutor.groups.filter(name='Profesores').exists():
        return False

    # comprobando cotutor
    if (not hasattr(tfg, 'cotutor')):
        return False
    elif not tfg.cotutor.groups.filter(name='Profesores').exists():
        return False

    tfg.save()
    return True


def update_tfg(tfg, campos):
    # comprobando titulo
    if 'titulo' in campos.keys():
        if campos['titulo'] == '' or not isinstance(campos['titulo'], str):
            return False
        else:
            tfg.titulo = campos['titulo']

    # comprobando tipo
    if 'tipo' in campos.keys():
        if campos['tipo'] == '' or not isinstance(campos['tipo'], str):
            return False
        else:
            tfg.tipo = campos['tipo']

    # comprobando n_alumnos
    if 'n_alumnos' in campos.keys():
        if (campos['n_alumnos'] <= 0) or (campos['n_alumnos'] > 3) or not (isinstance(campos['n_alumnos'], int)):
            return False
        else:
            tfg.n_alumnos = campos['n_alumnos']

    # comprobando descripcion
    if 'descripcion' in campos.keys():
        if campos['descripcion'] == '' or not isinstance(campos['descripcion'], str):
            return False
        else:
            tfg.descripcion = campos['descripcion']

    # comprobando conocimientos_previos
    if 'conocimientos_previos' in campos.keys():
        if campos['conocimientos_previos'] == '' or not isinstance(campos['conocimientos_previos'], str):
            return False
        else:
            tfg.conocimientos_previos = campos['conocimientos_previos']

    # comprobando hard_soft
    if 'hard_soft' in campos.keys():
        if campos['hard_soft'] == '' or not isinstance(campos['hard_soft'], str):
            return False
        else:
            tfg.hard_soft = campos['hard_soft']

    # comprobando tutor
    if 'tutor' in campos.keys():
        # NOTA: Cuando este el modelo de profesores, hay que ver que el tutor sea un profesor
        if not isinstance(campos['tutor'], Profesor) or not campos['tutor'].groups.filter(name='Profesores').exists():
            return False
        else:
            tfg.tutor = campos['tutor']

    # comprobando cotutor
    if 'cotutor' in campos.keys():
        # NOTA: Cuando este el modelo de profesores, hay que ver que el tutor sea un profesor
        if not isinstance(campos['cotutor'], Profesor) or not campos['cotutor'].groups.filter(name='Profesores').exists():
            return False
        else:
            tfg.tutor = campos['cotutor']

    tfg.save()

    return True


def delete_tfg(tfg):
    tfg.delete()

    try:
        Tfg.objects.get(titulo=tfg)
        return False
    except Tfg.DoesNotExist:
        return True


def asignar_tfg(tfg, alumno1, alumno2=None, alumno3=None):
    alumno2_ok = False
    alumno3_ok = False

    # Compruebo lo minimo para asignar el tfg
    if not isinstance(tfg, Tfg) or not isinstance(alumno1, Alumno) or not alumno1.groups.filter(
            name='Alumnos').exists() or existe_tfg_asig(alumno1):
        return False

    # Compruebo que no este ya asignado
    try:
        Tfg_Asig.objects.get(tfg=tfg)
        return False
    except Tfg_Asig.DoesNotExist:
        if comprueba_alumno(alumno2) and not existe_tfg_asig(alumno2):
            alumno2_ok = True
        if comprueba_alumno(alumno3) and not existe_tfg_asig(alumno3):
            alumno3_ok = True

        # Si tiene 2 alumnos
        if alumno2 != None and alumno3 == None:
            if not alumno2_ok:
                return False
            else:
                tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1, alumno_2=alumno2)
                tfg_asig.save()
                return True
        # Si tiene 3 alumnos
        elif alumno2 != None and alumno3 != None:
            if not alumno2_ok or not alumno3_ok:
                return False
            else:
                tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1, alumno_2=alumno2, alumno_3=alumno3)
                tfg_asig.save()
                return True
        # Si tiene 1 alumno
        else:
            tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1)
            tfg_asig.save()
            return True


def formar_comision(presidente, sup_presidente, titular_1, sup_titular_1, titular_2=None, sup_titular_2=None):

    if not (comprueba_profesor(presidente) and comprueba_profesor(sup_presidente)) or \
            not (comprueba_profesor(titular_1) and comprueba_profesor(sup_titular_1)):

        return False
    elif titular_2 and not (comprueba_profesor(titular_2) and comprueba_profesor(sup_titular_2)):
        return False
    else:
        comision = Comision_Evaluacion.objects.create(presidente=presidente, titular_1=titular_1,
                           titular_2=titular_2, sup_presidente=sup_presidente,
                           sup_titular_1=sup_titular_1, sup_titular_2=sup_titular_2)
        comision.save()
        return True
