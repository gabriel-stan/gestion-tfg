__author__ = 'tonima'

from gestion_tfg.servicios import tfg_services
from gestion_tfg.servicios import utils
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
    """

    #TODO: Aqui va la comprobacion del perfil del usuario

    if request.method == 'GET':
        alumno = Alumno.objects.all()
        serializer = AlumnoSerializer(alumno, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        params = utils.get_param(request)
        alumno = Alumno(username=params['username'], first_name=params['first_name'], last_name=params['last_name'])
        resul = tfg_services.insert_alumno(alumno)
        if resul['status']:
            return Response(resul)
        return Response(resul)
