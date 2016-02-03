__author__ = 'tonima'

from gestion_tfg.servicios import tfg_services
from gestion_tfg.servicios.utils import *
from gestion_tfg.models import Alumno
from gestion_tfg.serializers import AlumnoSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def alumnos(request):
    """
    Insertar un tfg nuevo
    :param request:
    :return :
    {status: True/False, data:{datos del alumno insertado o de todos los alumnos}
    """

    #TODO: Aqui va la comprobacion del perfil del usuario

    #Si es un GET, devuelvo la info de todos los alumnos
    if request.method == 'GET':
        alumno = Alumno.objects.all()
        serializer = AlumnoSerializer(alumno, many=True)
        return Response(serializer.data)

    #Si es un POST devuelvo la info del alumno nuevo
    elif request.method == 'POST':
        params = get_param(request)
        alumno = Alumno(username=params['username'], first_name=params['first_name'], last_name=params['last_name'])
        resul = tfg_services.insert_alumno(alumno)
        if resul['status']:
            return Response(to_dict(resul))
        return Response(resul)


@api_view(['POST'])
def update_alumnos(request):
    """
    Insertar un tfg nuevo
    :param request:
    :return :
    """

    #TODO: Aqui va la comprobacion del perfil del usuario

    params = get_param(request)
    alumno = Alumno.objects.get(username=params['username'])
    resul = tfg_services.update_alumno(alumno, params)
    if resul['status']:
        return Response(to_dict(resul))
    return Response(resul)