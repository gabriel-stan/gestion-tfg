__author__ = 'tonima'
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.servicios import tfg_services, utils
from model.models import Profesor


@api_view(['GET', 'POST'])
def profesores(request):
    """
    GET
    Obtener los datos de todos o de algun profesor
    :param request:
    :return :
    {status: True/False, data:{serializer del profesor o profesores}

    POST
    Insertar un profesor nuevo
    :param request:
    :return :
    {status: True/False, data:{datos del profesor insertado o de todos los profesores}
    """

    # TODO: Aqui va la comprobacion del perfil del usuario

    # Si es un GET, devuelvo la info de todos los profesores
    try:
        if request.method == 'GET':
            params = utils.get_params(request)
            if 'username' in params:
                resul = tfg_services.get_profesores(params['username'])
            else:
                resul = tfg_services.get_profesores()
            return Response(resul)

        # Si es un POST devuelvo la info del profesor nuevo
        elif request.method == 'POST':
            params = utils.get_params(request)
            profesor = Profesor(username=params['username'], first_name=params['first_name'],
                                last_name=params['last_name'], departamento=params['departamento'])
            resul = tfg_services.insert_profesor(profesor)
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Exception as e:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def update_profesor(request):
    """
    Actualizar datos de un profesor
    :param request: profesor <str>, campos <dict>
    :return :
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere actualizar
    try:
        if request.method == 'POST':
            params = utils.get_params(request)
            profesor = Profesor.objects.get(username=params['profesor'])
            resul = tfg_services.update_profesor(profesor, params['campos'])
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Profesor.DoesNotExist:
        return Response(dict(status=False, message="El profesor indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def delete_profesor(request):
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
                profesor = Profesor.objects.get(username=params['username'])
                resul = tfg_services.delete_profesor(profesor)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

    except Profesor.DoesNotExist:
        return Response(dict(status=False, message="El profesor indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))
