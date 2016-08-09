# -*- coding: utf-8 -*-
from eventos.models import Evento, Tipo_Evento, Periodo, SubTipo_Evento
from eventos.serializers import EventoSerializer, Tipo_EventoSerializer, SubTipo_EventoSerializer
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
            resul = utils.procesar_datos_eventos(request.user, self.serializer_class(eventos, many=True).data)
            self.logger.info('FIN WS - EVENTOSVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(status=True, data=resul), status=status.HTTP_200_OK)
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
                                                 tipo=params.get('tipo'),
                                                 convocatoria=params.get('convocatoria'),
                                                 titulo=params.get('titulo'),
                                                 sub_tipo=params.get('sub_tipo'),
                                                 autor=Usuario.objects.get(id=request.user.id),
                                                 desde=params.get('desde'), hasta=params.get('hasta'))

            if resul.get('status'):
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
            self.logger.info('INICIO WS - EVENTOSVIEW PUT del usuario: %s con params: %s' %
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
                self.logger.info('FIN WS - EVENTOSVIEW PUT del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - EVENTOSVIEW PUT del usuario: %s con resultado: %s' %
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
            self.logger.info('INICIO WS - EVENTOSVIEW DELETE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                evento = Evento.objects.get(contenido=params.get('contenido'))
                serializer = self.serializer_class(evento)
                resul = serializer.delete(evento)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.critical('FIN WS - EVENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul)

        except Evento.DoesNotExist:
            resul = dict(status=False, message="El evento indicado no existe")
            self.logger.error('INICIO WS - EVENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('INICIO WS - EVENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class Tipo_EventosViewSet(viewsets.ModelViewSet):
    lookup_field = 'codigo'
    queryset = Tipo_Evento.objects.order_by('-created_at')
    serializer_class = Tipo_EventoSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de los Tipos de eventos (convocatorias)
        :param request:
        :return :
        {status: True/False, data:{serializer de los tipos de eventos}

        """
        try:
            self.logger.info('INICIO WS - TIPO_EVENTOSVIEW LIST del usuario: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username))
            tipo_eventos = Tipo_Evento.objects.all()
            resul = self.serializer_class(tipo_eventos, many=True).data
            self.logger.info('FIN WS - TIPO_EVENTOSVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(status=True, data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            resul = dict(message=e.message)
            self.logger.error('TIPO_EVENTOSVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TIPO_EVENTOSVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un nuevo tipo de evento
        :param request:
        :return :
        {status: True/False, data:{datos del tipo de evento}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TIPO_EVENTOSVIEW CREATE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            resul = Tipo_Evento.objects.create(codigo=params.get('codigo'), nombre=params.get('nombre'))
            if resul.id:
                resul = utils.to_dict(dict(status=True, data=resul))
                resul_status = status.HTTP_200_OK
            else:
                resul = dict(message=resul['message'])
                resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.info('FIN WS - TIPO_EVENTOSVIEW CREATE del usuario: %s con params: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - TIPO_EVENTOSVIEW CREATE del usuario: %s con params: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Cambia los datos de un tipo de evento8
        :param request:
        :return :
        {status: True/False, data:{datos de la titulacion cambiada}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TIPO_EVENTOSVIEW PUT del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('eventos.tipo_evento.change') or request.user.is_admin:
                tipo_evento = Tipo_Evento.objects.get(codigo=params.get('codigo'))
                params = json.loads(params.get('data'))
                serializer = Tipo_EventoSerializer(tipo_evento)
                resul = serializer.update(tipo_evento, params)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                resul = dict(status=False, message="Sin privilegios")
                self.logger.info('FIN WS - TIPO_EVENTOSVIEW PUT del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - TIPO_EVENTOSVIEW PUT del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un tipo de evento
        :param request:
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TIPO_EVENTOSVIEW DELETE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                tipo_evento = Tipo_Evento.objects.get(codigo=params.get('codigo'))
                serializer = self.serializer_class(tipo_evento)
                resul = serializer.delete(tipo_evento)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.critical('FIN WS - TIPO_EVENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul)

        except Tipo_Evento.DoesNotExist:
            resul = dict(status=False, message="El tipo de evento indicado no existe")
            self.logger.error('INICIO WS - TIPO_EVENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('INICIO WS - TIPO_EVENTOSVIEW DELETE del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class SubTipo_EventosViewSet(viewsets.ModelViewSet):
    lookup_field = 'codigo'
    queryset = SubTipo_Evento.objects.order_by('-created_at')
    serializer_class = SubTipo_EventoSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de los subtipos de eventos
        :param request:
        :return :
        {status: True/False, data:{serializer de los eventos}

        """
        try:
            self.logger.info('INICIO WS - SUBTIPOEVENTOSVIEW LIST del usuario: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username))
            subtipo_eventos = SubTipo_Evento.objects.all()
            resul = self.serializer_class(subtipo_eventos, many=True).data
            self.logger.info('FIN WS - SUBTIPOEVENTOSVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(status=True, data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            resul = dict(message=e.message)
            self.logger.error('SUBTIPOEVENTOSVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('SUBTIPOEVENTOSVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un nuevo subtipo de evento
        :param request:
        :return :
        {status: True/False, data:{datos del subtipo de evento}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - SUBTIPOEVENTOSVIEW CREATE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            resul = SubTipo_Evento.objects.create(codigo=params.get('codigo'), nombre=params.get('nombre'))
            if resul.id:
                resul = utils.to_dict(dict(status=True, data=resul))
                resul_status = status.HTTP_200_OK
            else:
                resul = dict(message=resul['message'])
                resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.info('FIN WS - SUBTIPOEVENTOSVIEW CREATE del usuario: %s con params: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - SUBTIPOEVENTOSVIEW CREATE del usuario: %s con params: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Cambia los datos de un subtipo de evento
        :param request:
        :return :
        {status: True/False, data:{datos del subtipo de evento cambiado}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - SUBTIPOEVENTOSVIEW PUT del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('eventos.subtipo_eventos.change') or request.user.is_admin:
                subtipo = SubTipo_Evento.objects.get(codigo=params.get('codigo'))
                params = json.loads(params.get('datos'))
                serializer = SubTipo_EventoSerializer(subtipo)
                resul = serializer.update(subtipo, params)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                resul = dict(status=False, message="Sin privilegios")
                self.logger.info('FIN WS - SUBTIPOEVENTOSVIEW PUT del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - SUBTIPOEVENTOSVIEW PUT del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un subtipo de evento
        :param request:
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - SUBTIPOEVENTOSVIEW DELETE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                subtipo = SubTipo_Evento.objects.get(codigo=params.get('codigo'))
                serializer = self.serializer_class(subtipo)
                resul = serializer.delete(subtipo)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.critical('FIN WS - SUBTIPOEVENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul)

        except SubTipo_Evento.DoesNotExist:
            resul = dict(status=False, message="La titulacion indicada no existe")
            self.logger.error('INICIO WS - SUBTIPOEVENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('INICIO WS - SUBTIPOEVENTOSVIEW DELETE del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
