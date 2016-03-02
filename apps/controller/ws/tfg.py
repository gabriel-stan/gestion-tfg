__author__ = 'tonima'
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.servicios import tfg_services, utils
from model.models import Tfg


@api_view(['GET', 'POST'])
def tfgs(request):
    """
    GET
    Obtener los datos de todos o de algun tfg
    :param request:
    :return :
    {status: True/False, data:{serializer del tfg o tfgs}

    POST
    Insertar un tfg nuevo
    :param request:
    :return :
    {status: True/False, data:{datos del tfg insertado o de todos los tfgs}
    """

    # TODO: Aqui va la comprobacion del perfil del usuario

    # Si es un GET, devuelvo la info de todos los tfgs
    try:
        if request.method == 'GET':
            params = utils.get_params(request)
            if 'titulo' in params:
                resul = tfg_services.get_tfgs(titulo=params['titulo'])
            else:
                resul = tfg_services.get_tfgs()
            return Response(resul)

        # Si es un POST devuelvo la info del tfg nuevo
        elif request.method == 'POST':
            params = utils.get_params(request)
            tfg = Tfg(tipo=params['tipo'], titulo=params['titulo'], n_alumnos=params['n_alumnos'],
                      descripcion=params['descripcion'], conocimientos_previos=params['conocimientos_previos'],
                      hard_soft=params['hard_soft'],
                      tutor=params['tutor'], cotutor=params['cotutor'])
            resul = tfg_services.insert_tfg(tfg)
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Exception as e:
        return Response(dict(status=False, message="Error en la llamada"))

@api_view(['POST'])
def update_tfg(request):
    """
    Actualizar datos de un tfg
    :param request: tfg <str>, campos <dict>
    :return :
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere actualizar
    try:
        if request.method == 'POST':
            params = utils.get_params(request)
            tfg = Tfg.objects.get(titulo=params['titulo'])
            resul = tfg_services.update_tfg(tfg, params['campos'])
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Tfg.DoesNotExist:
        return Response(dict(status=False, message="El tfg indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def delete_tfg(request):
    """
    Eliminar un usuario
    :param request:
    :return :
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere borrar

    try:
        if request.method == 'POST':
            params = utils.get_params(request)
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params['titulo'])
                resul = tfg_services.delete_tfg(tfg)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

    except Tfg.DoesNotExist:
        return Response(dict(status=False, message="El tfg indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))
