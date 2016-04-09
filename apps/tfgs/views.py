# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from controller.servicios import tfg_services
from old.controller.servicios import utils
from model.models import Tfg
import servicios


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
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
                resul = servicios.get_tfgs(titulo=params['titulo'])
            else:
                resul = servicios.get_tfgs()
            return Response(resul)

        # Si es un POST devuelvo la info del tfg nuevo
        elif request.method == 'POST':
            per = request.user.get_all_permissions()
            # if not request.user.has_perm('model.add_tfg'):
            #     return Response(dict(status=False, message="No tiene los permisos necesarios"))
            # else:
            params = utils.get_params(request)
            tfg = Tfg(tipo=params['tipo'], titulo=params['titulo'], n_alumnos=params['n_alumnos'],
                      descripcion=params['descripcion'], conocimientos_previos=params['conocimientos_previos'],
                      hard_soft=params['hard_soft'],
                      tutor=params['tutor'], cotutor=params['cotutor'])
            resul = servicios.insert_tfg(tfg)
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
            resul = servicios.update_tfg(tfg, params['campos'])
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
                resul = servicios.delete_tfg(tfg)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

    except Tfg.DoesNotExist:
        return Response(dict(status=False, message="El tfg indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def asig_tfg(request):
    """
    POST
    Asignar un TFG a uno o varios alumnos
    :param request:
    :return :
    {status: True/False, data:{serializer del tfg asignado y de los alumnos}
    """

    # TODO: Aqui va la comprobacion del perfil del usuario

    try:
        if request.method == 'POST':
            # TODO: pasar los laumnos a un dict, cambiar aqui y en el servicio
            alumno2 = None
            alumno3 = None
            params = utils.get_params(request)
            tfg = servicios.get_tfgs(titulo=params['titulo'])['data'].serializer.instance
            alumno = tfg_services.get_alumnos(params['username'])['data'].serializer.instance
            if 'username2' in params:
                alumno2 = tfg_services.get_alumnos(params['username2'])['data'].serializer.instance
            if 'username3' in params:
                alumno3 = tfg_services.get_alumnos(params['username3'])['data'].serializer.instance
            resul = servicios.asignar_tfg(tfg, alumno, alumno2, alumno3)
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Exception as e:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def remove_asig_tfg(request):
    """
    POST
    Elimina la asignacion un TFG a uno o varios alumnos
    :param request:
    :return :
    {status: True/False, data:{serializer del tfg que ha quedado libre}
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere borrar

    try:
        if request.method == 'POST':
            params = utils.get_params(request)
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params['titulo'])
                resul = servicios.delete_tfg(tfg)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

    except Tfg.DoesNotExist:
        return Response(dict(status=False, message="El tfg indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))