# -*- coding: utf-8 -*-
from eventos.models import Evento
from eventos.serializers import EventoSerializer
from authentication.models import Usuario, Profesor
from rest_framework import viewsets, status, views
from rest_framework.response import Response
import json
import utils


class EventosViewSet(viewsets.ModelViewSet):
    lookup_field = 'contenido'
    queryset = Evento.objects.order_by('-created_at')
    serializer_class = EventoSerializer

    # def list(self, request):
    #     """
    #     GET
    #     Obtener los datos de todos o de algun tfg
    #     :param request:
    #     :return :
    #     {status: True/False, data:{serializer del tfg o tfgs}
    #
    #     """
    #     try:
    #         params = utils.get_params(request)
    #         if 'titulo' in params:
    #             tfg = Tfg.objects.get(titulo=params['titulo'])
    #             resul = self.serializer_class(tfg).data
    #         else:
    #             tfg = Tfg.objects.all()
    #             resul = self.serializer_class(tfg, many=True).data
    #             if len(resul) == 0:
    #                 raise NameError("No hay tfgs almacenados")
    #         return Response(dict(status=True, data=resul))
    #     except NameError as e:
    #         return Response(dict(status=False, message=e.message))
    #     except Tfg.DoesNotExist:
    #         return Response(dict(status=False, message="El tfg indicado no existe"))
    #     except Exception as e:
    #         return Response(dict(status=False, message="Error en la llamada"))

    def create(self, request):
        """
        POST
        Insertar un evento nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del evento}
        """
        try:
            request.data['autor'] = Usuario.objects.get(email=request.data['autor'])
            if 'cotutor' in request.data:
                request.data['cotutor'] = Profesor.objects.get(email=request.data['tutor'])
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                resul = Evento.objects.create_tfg(**serializer.validated_data)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                return Response(dict(status=False, message=serializer.errors), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)