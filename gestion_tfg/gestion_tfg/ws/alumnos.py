__author__ = 'tonima'

from gestion_tfg.models import Tfg
from gestion_tfg.servicios import utils
from gestion_tfg.models import Alumno
from gestion_tfg.serializers import AlumnoSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

@csrf_exempt
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
        serializer = AlumnoSerializer(data=params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)