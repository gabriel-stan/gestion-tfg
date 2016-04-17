# -*- coding: utf-8 -*-
from tfgs.models import Tfg, Tfg_Asig
from tfgs.serializers import TfgSerializer, Tfg_AsigSerializer
from authentication.models import Alumno, Profesor
from rest_framework import viewsets, status
from rest_framework.response import Response
import json
import utils


class TfgViewSet(viewsets.ModelViewSet):
    lookup_field = 'titulo'
    queryset = Tfg.objects.all()
    serializer_class = TfgSerializer

    def list(self, request):
        """
        GET
        Obtener los datos de todos o de algun tfg
        :param request:
        :return :
        {status: True/False, data:{serializer del tfg o tfgs}

        """
        try:
            params = utils.get_params(request)
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params['titulo'])
                resul = self.serializer_class(tfg).data
            else:
                tfg = Tfg.objects.all()
                resul = self.serializer_class(tfg, many=True).data
                if len(resul) == 0:
                    raise NameError("No hay tfgs almacenados")
            return Response(dict(status=True, data=resul))
        except NameError as e:
            return Response(dict(status=False, message=e.message))
        except Tfg.DoesNotExist:
            return Response(dict(status=False, message="El tfg indicado no existe"))
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"))

    def create(self, request):
        """
        POST
        Insertar un tfg nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del tfg insertado o de todos los tfgs}
        """
        try:
            if request.user.has_perm('tfgs.can_create_tfgs') or request.user.is_admin:
                request.data['tutor'] = Profesor.objects.get(email=request.data['tutor'])
                if 'cotutor' in request.data:
                    request.data['cotutor'] = Profesor.objects.get(email=request.data['tutor'])
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    resul = Tfg.objects.create_tfg(**serializer.validated_data)
                    if resul['status']:
                        return Response(utils.to_dict(resul))
                    else:
                        return Response(resul)
                else:
                    return Response(dict(status=False, message=serializer.errors), status=status.HTTP_200_OK)
            else:
                return Response(dict(status=False, message="Sin privilegios"),
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Actualizar datos de un tfg
        :param request: tfg <str>, campos <dict>
        :return :
        """

        try:
            if request.user.has_perm('tfgs.can_change_tfgs') or request.user.is_admin:
                tfg = Tfg.objects.get(titulo=request.data['titulo'])
                params = json.loads(request.data['datos'])
                serializer = self.serializer_class(tfg)
                resul = serializer.update(tfg, params)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                return Response(dict(status=False, message="Sin privilegios"),
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un usuario
        :param request:
        :return :
        """

        try:
            params = utils.get_params(request)
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params['titulo'])
                serializer = self.serializer_class(tfg)
                resul = serializer.delete_tfg(tfg)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

        except Tfg.DoesNotExist:
            return Response(dict(status=False, message="El tfg indicado no existe"))
        except Exception:
            return Response(dict(status=False, message="Error en la llamada"))


class Tfg_asigViewSet(viewsets.ModelViewSet):
    lookup_field = 'tfg'
    queryset = Tfg_Asig.objects.all()
    serializer_class = Tfg_AsigSerializer

    def post(self, request):
        """
        POST
        Asignar un TFG a uno o varios alumnos
        :param request:
        :return:
        {status: True/False, data:{serializer del tfg asignado y de los alumnos}
        """

        try:
            alumno_2 = None
            alumno_3 = None
            params = utils.get_params(request)
            tfg = Tfg.objects.get(titulo=params['tfg'])
            alumno_1 = Alumno.objects.get(email=params['alumno1'])
            if 'alumno_2' in params:
                alumno_2 = Alumno.objects.get(email=params['alumno_2'])
            if 'alumno_3' in params:
                alumno_3 = Alumno.objects.get(email=params['alumno_3'])
            serializer = self.serializer_class(data=dict(tfg=tfg, alumno_1=alumno_1, alumno_2=alumno_2,
                                                         alumno_3=alumno_3))
            if serializer.is_valid():
                resul = Tfg_Asig.objects.create_tfg(**serializer.validated_data)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                return Response(dict(status=False, message=serializer.errors), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"))

    def delete(self, request):
        """
        DELETE
        Elimina la asignacion un TFG a uno o varios alumnos
        :param request:
        :return :
        {status: True/False, data:{serializer del tfg que ha quedado libre}
        """

        try:
            params = utils.get_params(request)
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params['titulo'])
                tfg_asig = Tfg_Asig.objects.get(tfg=tfg)
                serializer = self.serializer_class(tfg_asig)
                resul = serializer.delete_tfg(tfg_asig)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

        except Tfg.DoesNotExist:
            return Response(dict(status=False, message="El tfg indicado no existe"))
        except Exception:
            return Response(dict(status=False, message="Error en la llamada"))