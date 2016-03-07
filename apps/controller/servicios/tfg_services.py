# -*- coding: utf-8 -*-
import re
import utils
from model.models import Comision_Evaluacion, Alumno, Tfg, Tfg_Asig, Profesor
from model.serializers import AlumnoSerializer, ProfesorSerializer, TFGSerializer
from django.contrib.auth.models import Group
from openpyxl import load_workbook


def get_alumnos(username=None):
    try:
        if username:
            alumno = Alumno.objects.get(username=str(username))
            resul = AlumnoSerializer(alumno).data
        else:
            alumno = Alumno.objects.all()
            resul = AlumnoSerializer(alumno, many=True).data
            if len(resul) == 0:
                raise NameError("No hay alumnos almacenados")

        return dict(status=True, data=resul)
    except NameError as e:
        return dict(status=False, message=e.message)
    except Alumno.DoesNotExist:
        return dict(status=False, message="El alumno indicado no existe")


def insert_alumno(alumno):
    try:
        if not alumno.username:
            raise NameError("Error en el nombre del alumno")
        else:
            res = Alumno.objects.filter(username=alumno.username)
            if res.count() != 0:
                raise NameError("El alumno ya existe")

        if not alumno.first_name or not utils.is_string(alumno.first_name):
            raise NameError("Nombre incorrecto")

        if not alumno.last_name or not utils.is_string(alumno.last_name):
            raise NameError("Apellidos incorrectos")

        # exp reg para saber si el nick corresponde al correo de la ugr (@correo.ugr.es)
        if not re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$', alumno.username):
            raise NameError("El correo no es correcto")

        grupo_alumnos = Group.objects.get_or_create(name='Alumnos')
        alumno.save()
        alumno.groups.add(grupo_alumnos[0])

        return dict(status=True, data=Alumno.objects.get(username=alumno.username))

    except NameError as e:
        return dict(status=False, message=e.message)


def update_alumno(alumno, campos):
    try:
        # comprobando username
        if 'username' in campos.keys():
            res = Alumno.objects.filter(username=campos['username'])
            if res.count() == 0:
                if not utils.is_string(campos['username']) or not re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$',
                                                                           campos['username']):
                    raise NameError("El correo no es correcto")
                else:
                    alumno.username = campos['username']
            else:
                raise NameError("El alumno indicado no existe")

        # comprobando nombre
        if 'first_name' in campos.keys():
            if campos['first_name'] == '' or not utils.is_string(campos['first_name']):
                raise NameError("Nombre incorrecto")
            else:
                alumno.first_name = campos['first_name']

        # comprobando apellidos
        if 'last_name' in campos.keys():
            if campos['last_name'] == '' or not utils.is_string(campos['last_name']):
                raise NameError("Apellidos incorrectos")
            else:
                alumno.last_name = campos['last_name']

        alumno.save()

        return dict(status=True, data=Alumno.objects.get(username=alumno.username))

    except NameError as e:
        return dict(status=False, message=e.message)
    except:
        return dict(status=False, message="El correo no es correcto")


def delete_alumno(alumno):

    try:
        Alumno.objects.get(username=alumno.username).delete()
        return dict(status=True)
    except Alumno.DoesNotExist:
        return dict(status=False, message="El alumno no existe")


def get_profesores(username=None):
    try:
        if username:
            profesor = Profesor.objects.get(username=str(username))
            resul = ProfesorSerializer(profesor).data
        else:
            profesor = Profesor.objects.all()
            resul = ProfesorSerializer(profesor, many=True).data
            if len(resul) == 0:
                raise NameError("No hay profesores almacenados")

        return dict(status=True, data=resul)
    except NameError as e:
        return dict(status=False, message=e.message)
    except Profesor.DoesNotExist:
        return dict(status=False, message="El profesor indicado no existe")


def insert_profesor(profesor):

    try:
        if not profesor.username or not (re.match(r'^[a-z][_a-z0-9]+(@ugr\.es)$', profesor.username)):
            raise NameError("El correo no es correcto")
        else:
            res = Profesor.objects.filter(username=profesor.username)
            if res.count() != 0:
                raise NameError("El profesor ya existe")

        if not profesor.first_name or not utils.is_string(profesor.first_name):
            raise NameError("Error en el nombre del profesor")

        if not profesor.last_name or not utils.is_string(profesor.last_name):
            raise NameError("Error en los apellidos del profesor")

        if not profesor.departamento or not utils.is_string(profesor.departamento):
            raise NameError("Error en el departamento")

        grupo_profesores = Group.objects.get_or_create(name='Profesores')
        profesor.save()
        profesor.groups.add(grupo_profesores[0])

        return dict(status=True, data=Profesor.objects.get(username=profesor.username))

    except NameError as e:
        return dict(status=False, message=e.message)


def update_profesor(profesor, campos):
    try:
        # comprobando username
        if 'username' in campos.keys():
            res = Profesor.objects.filter(username=campos['username'])
            if res.count() == 0:
                if not (re.match(r'^[a-z][_a-z0-9]+(@ugr\.es)$', campos['username'])):
                    raise NameError("El correo no es correcto")
                else:
                    profesor.username = campos['username']
            else:
                raise NameError("No existe el profesor")

        # comprobando nombre
        if 'first_name' in campos.keys():
            if campos['first_name'] == '' or not utils.is_string(campos['first_name']):
                raise NameError("Error en el nombre del profesor")
            else:
                profesor.first_name = campos['first_name']

        # comprobando apellidos
        if 'last_name' in campos.keys():
            if campos['last_name'] == '' or not utils.is_string(campos['last_name']):
                raise NameError("Error en los apellidos del profesor")
            else:
                profesor.last_name = campos['last_name']

        # comprobando departamento
        if 'departamento' in campos.keys():
            if campos['departamento'] == '' or not utils.is_string(campos['departamento']):
                raise NameError("Error en el departamento")
            else:
                profesor.departamento = campos['departamento']

        profesor.save()

        return dict(status=True, data=Profesor.objects.get(username=profesor.username))

    except NameError as e:
        return dict(status=False, message=e.message)
    except:
        return dict(status=False, message="El correo no es correcto")


def delete_profesor(profesor):

    try:
        Profesor.objects.get(username=profesor.username).delete()
        return dict(status=True)
    except Profesor.DoesNotExist:
        return dict(status=False, message="El profesor no existe")


# obtener todos los tfgs o solo por id y que el front filtre, e ahi la cuestion...
def get_tfgs(titulo=None):
    try:
        if titulo:
            tfg = Tfg.objects.get(titulo=titulo)
            resul = TFGSerializer(tfg).data
        else:
            tfg = Tfg.objects.all()
            resul = TFGSerializer(tfg, many=True).data
            if len(resul) == 0:
                raise NameError("No hay tfgs almacenados")

        return dict(status=True, data=resul)
    except NameError as e:
        return dict(status=False, message=e.message)
    except Tfg.DoesNotExist:
        return dict(status=False, message="El tfg indicado no existe")


def insert_tfg(tfg):
    try:
        # comprobando titulo vacio o Tfg con el mismo titulo
        if not tfg.titulo:
            raise NameError("Titulo necesario")
        else:
            res = Tfg.objects.filter(titulo=tfg.titulo)
            if res.count() != 0:
                raise NameError("El TFG ya existe")

        # comprobando tipo no vacio
        if not tfg.tipo:
            raise NameError("Tipo de TFG necesario")

        # comprobando numero de alumnos
        if tfg.n_alumnos is None or not utils.is_int(tfg.n_alumnos) or int(tfg.n_alumnos) <= 0 \
                or int(tfg.n_alumnos) > 3:
            raise NameError("Numero de alumnos incorrecto")

        # comprobando descripcion
        if not tfg.descripcion:
            raise NameError("Descripcion necesaria")

        # comprobando tutor
        if not hasattr(tfg, 'tutor'):
            raise NameError("Tutor necesario")
        elif not tfg.tutor.groups.filter(name='Profesores').exists():
            raise NameError("Tutor ha de ser un profesor")

        # comprobando cotutor
        if hasattr(tfg, 'cotutor') and tfg.cotutor:
            if not tfg.cotutor.groups.filter(name='Profesores').exists():
                raise NameError("Cotutor ha de ser un profesor")

        tfg.save()
        return dict(status=True, data=Tfg.objects.get(titulo=tfg.titulo))

    except NameError as e:
        return dict(status=False, message=e.message)


def update_tfg(tfg, campos):

    try:
        # comprobando titulo
        if 'titulo' in campos.keys():
            if campos['titulo'] == '' or not utils.is_string(campos['titulo']):
                raise NameError("Titulo incorrecto")
            else:
                tfg.titulo = campos['titulo']

        # comprobando tipo
        if 'tipo' in campos.keys():
            if campos['tipo'] == '' or not utils.is_string(campos['tipo']):
                raise NameError("Tipo incorrecto")
            else:
                tfg.tipo = campos['tipo']

        # comprobando n_alumnos
        if 'n_alumnos' in campos.keys():
            if (campos['n_alumnos'] <= 0) or (campos['n_alumnos'] > 3) or not (isinstance(campos['n_alumnos'], int)):
                raise NameError("Numero de alumnos incorrecto")
            else:
                tfg.n_alumnos = campos['n_alumnos']

        # comprobando descripcion
        if 'descripcion' in campos.keys():
            if campos['descripcion'] == '' or not utils.is_string(campos['descripcion']):
                raise NameError("Descripcion incorrecta")
            else:
                tfg.descripcion = campos['descripcion']

        # comprobando conocimientos_previos
        if 'conocimientos_previos' in campos.keys():
            if campos['conocimientos_previos'] == '' or not utils.is_string(campos['conocimientos_previos']):
                raise NameError("Conocimientos Previos incorrectos")
            else:
                tfg.conocimientos_previos = campos['conocimientos_previos']

        # comprobando hard_soft
        if 'hard_soft' in campos.keys():
            if campos['hard_soft'] == '' or not utils.is_string(campos['hard_soft']):
                raise NameError("Hard/Soft incorrectos")
            else:
                tfg.hard_soft = campos['hard_soft']

        # comprobando tutor
        if 'tutor' in campos.keys():
            if not isinstance(campos['tutor'], Profesor) or not campos['tutor'].groups.filter(
                    name='Profesores').exists():
                raise NameError("Tutor incorrecto")
            else:
                tfg.tutor = campos['tutor']

        # comprobando cotutor
        if 'cotutor' in campos.keys():
            if not isinstance(campos['cotutor'], Profesor) or not campos['cotutor'].groups.filter(
                    name='Profesores').exists():
                raise NameError("CoTutor incorrecto")
            else:
                tfg.tutor = campos['cotutor']

        tfg.save()

        return dict(status=True, data=Tfg.objects.get(titulo=tfg.titulo))
    except NameError as e:
        return dict(status=False, message=e.message)


def delete_tfg(tfg):

    try:
        Tfg.objects.get(titulo=tfg.titulo).delete()
        return dict(status=True)
    except Tfg.DoesNotExist:
        return dict(status=False, message="El TFG no existe")


def asignar_tfg(tfg, alumno1, alumno2=None, alumno3=None):
    alumno2_ok = False
    alumno3_ok = False
    try:
        # Compruebo lo minimo para asignar el tfg
        if not isinstance(tfg, Tfg) or not isinstance(alumno1, Alumno) or not alumno1.groups.filter(
                name='Alumnos').exists() or utils.existe_tfg_asig(alumno1):
            raise NameError("Error en los parametros de entrada")

        # Compruebo que no este ya asignado
        try:
            Tfg_Asig.objects.get(tfg=tfg)
            raise NameError("Tfg ya asignado")
        except Tfg_Asig.DoesNotExist:
            if utils.comprueba_alumno(alumno2) and not utils.existe_tfg_asig(alumno2):
                alumno2_ok = True
            if utils.comprueba_alumno(alumno3) and not utils.existe_tfg_asig(alumno3):
                alumno3_ok = True

            # Si tiene 2 alumnos
            if alumno2 and not alumno3:
                if not alumno2_ok:
                    raise NameError("Error en el segundo alumno")
                else:
                    tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1, alumno_2=alumno2)
                    tfg_asig.save()
            # Si tiene 3 alumnos
            elif alumno2 and alumno3:
                if not alumno2_ok or not alumno3_ok:
                    raise NameError("Error en el tercer alumno")
                else:
                    tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1, alumno_2=alumno2, alumno_3=alumno3)
                    tfg_asig.save()
            # Si tiene 1 alumno
            else:
                tfg_asig = Tfg_Asig.objects.create(tfg=tfg, alumno_1=alumno1)
                tfg_asig.save()

            return dict(status=True, data=Tfg_Asig.objects.get(tfg=tfg))

    except NameError as e:
        return dict(status=False, message=e.message)


def formar_comision(presidente, sup_presidente, titular_1, sup_titular_1, titular_2=None, sup_titular_2=None):

    try:
        if not (utils.comprueba_profesor(presidente) and utils.comprueba_profesor(sup_presidente)) or \
                not (utils.comprueba_profesor(titular_1) and utils.comprueba_profesor(sup_titular_1)):

            raise NameError("Error en los miembros del comite")
        elif titular_2 and not (utils.comprueba_profesor(titular_2) and utils.comprueba_profesor(sup_titular_2)):
            raise NameError("Error en los suplentes del comite")
        else:
            comision = Comision_Evaluacion.objects.create(presidente=presidente, titular_1=titular_1,
                                                          titular_2=titular_2, sup_presidente=sup_presidente,
                                                          sup_titular_1=sup_titular_1, sup_titular_2=sup_titular_2)
            comision.save()
        return dict(status=True, data=comision)
    except NameError as e:
        return dict(status=False, message=e.message)


def subida_masiva(fichero, filas):
    wb = load_workbook(fichero)
    ws = wb.active
    errores = []
    for i in range(5, 5+filas):
        datos = dict(tipo=ws['D' + str(i)].value,
                     titulo=ws['E' + str(i)].value,
                     n_alumnos=ws['F' + str(i)].value, descripcion=ws['G' + str(i)].value,
                     conocimientos_previos=ws['H' + str(i)].value,
                     hard_soft=ws['I' + str(i)].value)
        if not datos['titulo']:
            errores.append(ws['A' + str(i)].value)
            continue
        try:
            datos['tutor'] = Profesor.objects.get(username=str(ws['B' + str(i)].value))
            if ws['C' + str(i)].value:
                datos['cotutor'] = Profesor.objects.get(username=str(ws['C' + str(i)].value))
                tfg = Tfg(tipo=datos['tipo'], titulo=datos['titulo'], n_alumnos=datos['n_alumnos'],
                          descripcion=datos['descripcion'], conocimientos_previos=datos['conocimientos_previos'],
                          hard_soft=datos['hard_soft'],
                          tutor=datos['tutor'], cotutor=datos['cotutor'])
            else:
                tfg = Tfg(tipo=datos['tipo'], titulo=datos['titulo'], n_alumnos=datos['n_alumnos'],
                          descripcion=datos['descripcion'], conocimientos_previos=datos['conocimientos_previos'],
                          hard_soft=datos['hard_soft'],
                          tutor=datos['tutor'])
            insert_tfg(tfg)
        except Profesor.DoesNotExist:
            errores.append(dict(fila=ws['A' + str(i)].value, message='El profesor no existe'))
            continue
        except Exception as e:
            errores.append(dict(fila=ws['A' + str(i)].value, message=e.message))
            continue
    return dict(status=True, data=errores)
