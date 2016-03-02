__author__ = 'tonima'
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.servicios import tfg_services, utils
from model.models import Tfg


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
            tfg = tfg_services.get_tfgs(titulo=params['titulo'])['data'].serializer.instance
            alumno = tfg_services.get_alumnos(params['username'])['data'].serializer.instance
            if 'username2' in params:
                alumno2 = tfg_services.get_alumnos(params['username2'])['data'].serializer.instance
            if 'username3' in params:
                alumno3 = tfg_services.get_alumnos(params['username3'])['data'].serializer.instance
            resul = tfg_services.asignar_tfg(tfg, alumno, alumno2, alumno3)
            if resul['status']:
                return Response(utils.to_dict(resul))
            return Response(resul)

    except Exception as e:
        return Response(dict(status=False, message="Error en la llamada"))


@api_view(['POST'])
def delete_asig_tfg(request):
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
                resul = tfg_services.delete_tfg(tfg)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

    except Tfg.DoesNotExist:
        return Response(dict(status=False, message="El tfg indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))
