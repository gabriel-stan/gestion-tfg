__author__ = 'tonima'
from old.controller.servicios import utils
from old.model import Alumno, Tfg, Tfg_Asig, Profesor
from old.model import TFGSerializer


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