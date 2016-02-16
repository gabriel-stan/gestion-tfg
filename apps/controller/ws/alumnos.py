__author__ = 'tonima'
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.servicios import tfg_services, utils
from model.models import Alumno
from model.serializers import AlumnoSerializer


@api_view(['GET', 'POST'])
def alumnos(request):
    """
    Insertar un alumno nuevo
    :param request:
    :return :
    {status: True/False, data:{datos del alumno insertado o de todos los alumnos}
    """

    #TODO: Aqui va la comprobacion del perfil del usuario

    #Si es un GET, devuelvo la info de todos los alumnos
    if request.method == 'GET':
        resul = {}
        alumno = Alumno.objects.all()
        serializer = AlumnoSerializer(alumno, many=True)
        if len(serializer.data) != 0:
            resul['status'] = True
            resul['data'] = serializer.data
            return Response(resul)
        else:
            resul['status'] = False
            return Response(resul)

    #Si es un POST devuelvo la info del alumno nuevo
    elif request.method == 'POST':
        params = utils.get_param(request)
        alumno = Alumno(username=params['username'], first_name=params['first_name'], last_name=params['last_name'])
        resul = tfg_services.insert_alumno(alumno)
        if resul['status']:
            return Response(utils.to_dict(resul))
        return Response(resul)


@api_view(['POST'])
def update_alumno(request):
    """
    Actualizar datos de un alumno
    :param request:
    :return :
    """

    #TODO: Aqui va la comprobacion del perfil del usuario que quiere actualizar

    params = utils.get_param(request)
    alumno = Alumno.objects.get(username=params['username'])
    resul = tfg_services.update_alumno(alumno, params)
    if resul['status']:
        return Response(utils.to_dict(resul))
    return Response(resul)


@api_view(['POST'])
def delete_alumno(request):
    """
    Eliminar un usuario
    :param request:
    :return :
    """

    #TODO: Aqui va la comprobacion del perfil del usuario que quiere borrar

    params = utils.get_param(request)
    alumno = Alumno.objects.get(username=params['username'])
    resul = tfg_services.delete_alumno(alumno)
    if resul['status']:
        return Response(utils.to_dict(resul))
    return Response(resul)