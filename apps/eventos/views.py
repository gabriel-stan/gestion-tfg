# -*- coding: utf-8 -*-
from eventos.models import Evento, Tipo_Evento
from eventos.serializers import EventoSerializer
from authentication.models import Usuario
from rest_framework import viewsets, status
from rest_framework.response import Response
import utils
import json
import logging


class EventosViewSet(viewsets.ModelViewSet):
    lookup_field = 'contenido'
    queryset = Evento.objects.order_by('-created_at')
    serializer_class = EventoSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de los eventos
        :param request:
        :return :
        {status: True/False, data:{serializer de los eventos}

        """
        try:
            self.logger.info('INICIO WS - EVENTOSVIEW LIST del usuario: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username))
            eventos = Evento.objects.all()
            resul = self.serializer_class(eventos, many=True).data
            self.logger.info('FIN WS - EVENTOSVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            resul = dict(message=e.message)
            self.logger.error('EVENTOSVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('EVENTOSVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un evento nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del evento}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - EVENTOSVIEW CREATE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            resul = Evento.objects.create_evento(contenido=params.get('contenido'),
                                                 tipo=Tipo_Evento.objects.get(codigo=params.get('tipo')),
                                                 titulo=params.get('titulo'), desde=params.get('desde'),
                                                 hasta=params.get('hasta'),
                                                 autor=Usuario.objects.get(id=request.user.id))
            if resul['status']:
                resul = utils.to_dict(resul)
                resul_status = status.HTTP_200_OK
            else:
                resul = dict(message=resul['message'])
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - EVENTOSVIEW CREATE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('EVENTOSVIEW CREATE: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Cambia los datos de un evento
        :param request:
        :return :
        {status: True/False, data:{datos del evento cambiado}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - DEPARTAMENTOSVIEW PUT del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('eventos.evento.change') or request.user.is_admin:
                evento = Evento.objects.get(contenido=params.get('contenido'))
                params = json.loads(params.get('data'))
                serializer = EventoSerializer(evento)
                resul = serializer.update(evento, params)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                resul = dict(status=False, message="Sin privilegios")
                self.logger.info('FIN WS - DEPARTAMENTOSVIEW PUT del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - DEPARTAMENTOSVIEW PUT del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un evento
        :param request:
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                evento = Evento.objects.get(contenido=params.get('contenido'))
                serializer = self.serializer_class(evento)
                resul = serializer.delete(evento)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.critical('FIN WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul)

        except Evento.DoesNotExist:
            resul = dict(status=False, message="El evento indicado no existe")
            self.logger.error('INICIO WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('INICIO WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
