# -*- coding: utf-8 -*-
from rest_framework import status, views
from rest_framework.response import Response
from service import Tfgs_masivos, Tfgs_asig_masivos
from django.apps import apps
from utils import get_model
import django.apps
import utils
import json
import logging

SUBIDAS={'tfg': Tfgs_masivos, 'tfg_asig': Tfgs_asig_masivos}


class Upload_fileView(views.APIView):
    logger = logging.getLogger(__name__)

    def post(self, request):
        """
        POST
        Subir un fichero de TFGs
        :param request:
        :return :

        """
        try:
            self.logger.info('INICIO WS - UPLOADFILEVIEW POST del usuario: %s con parametros: %s' % (request.user.email if hasattr(request.user, 'email') else request.user.username, request.FILES['file']))
            if request.user.has_perm('tfgs.tfg.masivos') or request.user.is_admin:
                file = request.FILES['file']
                u_fila = int(request.POST['u_fila'])
                p_fila = int(request.POST['p_fila'])
                cabeceras = json.loads(request.POST['cabeceras'])
                tipe_file = str(request.POST['tipe_file'])
                load_tfgs = SUBIDAS.get(tipe_file)(file)
                titulacion = str(request.POST['titulacion'])
                resul = load_tfgs.upload_file_tfg(u_fila, p_fila, cabeceras, titulacion)
                if resul['status']:
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - UPLOADFILEVIEW POST del usuario: %s con resultado: %s' % (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('UPLOADFILEVIEW POST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class Upload_file_confirmView(views.APIView):
    logger = logging.getLogger(__name__)

    def post(self, request):
        """
        POST
        Confirma y crea los tfgs devolviendo los errores
        :param request:
        :return :

        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - UPLOADFILECONFIRMVIEW POST del usuario: %s con parametros: %s' % (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('tfgs.tfg.masivos') or request.user.is_admin:
                model = get_model(params.get('model'))
                load_tfgs = SUBIDAS.get(params.get('model'))()
                resul = load_tfgs.upload_file_confirm(params['list_tfg'])
                if resul['status']:
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - UPLOADFILECONFIRMVIEW POST del usuario: %s con resultado: %s' % (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('UPLOADFILECONFIRMVIEW POST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
