# -*- coding: utf-8 -*-
from tfgs.models import Tfg, Tfg_Asig
from tfgs.serializers import TfgSerializer, Tfg_AsigSerializer
from authentication.models import Alumno, Profesor
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from service import upload_file_tfg
import json
import utils


class Upload_fileView(views.APIView):
    lookup_field = 'titulo'
    queryset = Tfg.objects.all()
    serializer_class = TfgSerializer

    def post(self, request):
        """
        POST
        Subir un fichero de TFGs
        :param request:
        :return :
        {status: True/False, data:{datos del tfg insertado o de todos los tfgs}
        """
        try:
            if request.user.has_perm('tfgs.tfg.create') or request.user.is_admin:
                file = request.FILES['file']
                filas = int(request.POST['filas'])
                p_fila = int(request.POST['p_fila'])
                cabeceras = json.loads(request.POST['cabeceras'])
                resul = upload_file_tfg(file, filas, p_fila, cabeceras)
                if resul['status']:
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            return Response(resul, status=resul_status)
        except Exception as e:
            return Response(dict(message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)