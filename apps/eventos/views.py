# -*- coding: utf-8 -*-
from eventos.models import Evento
from eventos.serializers import EventoSerializer
from authentication.models import Usuario, Profesor
from authentication.serializers import UsuarioSerializer
from rest_framework import viewsets, status, views
from rest_framework.response import Response
import json
import utils


class EventosViewSet(viewsets.ModelViewSet):
    lookup_field = 'contenido'
    queryset = Evento.objects.order_by('-created_at')
    serializer_class = EventoSerializer

    def list(self, request):
        """
        GET
        Obtener los datos de los eventos
        :param request:
        :return :
        {status: True/False, data:{serializer de los eventos}

        """
        try:
            # eventos = Evento.objects.filter(autor=request.user.id)
            eventos = Evento.objects.all()
            resul = self.serializer_class(eventos, many=True).data
            return Response(dict(data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            return Response(dict(message=e.message), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(dict(message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un evento nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del evento}
        """
        try:
            content = request.data['content']
            tipo = 'info'
            # serializer = self.serializer_class(data={'contenido': content, 'tipo': tipo, 'autor': request.user.id})
            # if serializer.is_valid():
            #     resul = serializer.create_evento(serializer.validated_data)
            #     if resul['status']:
            #         return Response(utils.to_dict(resul))
            #     else:
            #         return Response(resul)
            # else:
            #     return Response(dict(status=False, message=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            resul = Evento.objects.create_evento(contenido=content, tipo=tipo, autor=Usuario.objects.get(id=request.user.id))
            if resul['status']:
                resul = utils.to_dict(resul)
                resul_status = status.HTTP_200_OK
            else:
                resul = dict(message=resul['message'])
                resul_status = status.HTTP_400_BAD_REQUEST
            return Response(resul, status=resul_status)
        except Exception as e:
            return Response(dict(message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)