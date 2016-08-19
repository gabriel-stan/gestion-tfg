# -*- coding: utf-8 -*-
from tfgs.models import Tfg, Tfg_Asig, Titulacion
from rest_framework import viewsets, status, views
from rest_framework.response import Response
import logging


class EstadisticaView(views.APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):
        self.logger.info('INICIO WS - ESTADISTICASVIEW GET del usuario: %s' %
                         request.user.email if hasattr(request.user, 'email') else request.user.username)
        tfgs = Tfg.objects.all().count()
        tfgs_asig = Tfg_Asig.objects.all().count()
        resul = {'status': True, 'data': {'tfgs': tfgs, 'tfgs_asig': tfgs_asig}}
        self.logger.info('FIN WS - ESTADISTICASVIEW GET del usuario: %s, con resultado: %s' %
                         (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
        return Response(resul, status=status.HTTP_200_OK)