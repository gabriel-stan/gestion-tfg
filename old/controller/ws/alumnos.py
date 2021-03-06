__author__ = 'tonima'
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from controller.servicios import tfg_services
from old.controller.servicios import utils
from model.models import Alumno


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def alumnos(request):
    """
    GET
    Obtener los datos de todos o de algun alumno
    :param request:
    :return :
    {status: True/False, data:{serializer del alumno o alumnos}

    POST
    Insertar un alumno nuevo
    :param request:
    :return :
    {status: True/False, data:{datos del alumno insertado o de todos los alumnos}
    """

    # TODO: Aqui va la comprobacion del perfil del usuario

    # Si es un GET, devuelvo la info de todos los alumnos
    try:
        if request.method == 'GET':
            params = utils.get_params(request)
            if 'username' in params:
                resul = tfg_services.get_alumnos(params['username'])
            else:
                resul = tfg_services.get_alumnos()
            return Response(resul)

        # Si es un POST devuelvo la info del alumno nuevo
        elif request.method == 'POST':
            params = utils.get_params(request)
            alumno = Alumno(username=params['username'], first_name=params['first_name'], last_name=params['last_name'],
                            password=params['password'])
            resul = tfg_services.insert_alumno(alumno)
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Exception as e:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def update_alumno(request):
    """
    Actualizar datos de un alumno
    :param request: alumno <str>, campos <dict>
    :return :
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere actualizar
    try:
        if request.method == 'POST':
            params = utils.get_params(request)
            alumno = Alumno.objects.get(username=params['alumno'])
            resul = tfg_services.update_alumno(alumno, params['campos'])
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Alumno.DoesNotExist:
        return Response(dict(status=False, message="El alumno indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def delete_alumno(request):
    """
    Eliminar un usuario
    :param request:
    :return :
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere borrar

    try:
        if request.method == 'POST':
            params = utils.get_params(request)
            if 'username' in params:
                alumno = Alumno.objects.get(username=params['username'])
                resul = tfg_services.delete_alumno(alumno)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

    except Alumno.DoesNotExist:
        return Response(dict(status=False, message="El alumno indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))
