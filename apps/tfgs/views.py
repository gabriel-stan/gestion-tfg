# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from tfgs.models import Tfg, Tfg_Asig, Titulacion
from tfgs.serializers import TfgSerializer, Tfg_AsigSerializer, TitulacionSerializer
from authentication.models import Alumno, Profesor
from rest_framework import viewsets, status, views
from rest_framework.response import Response
import json
import utils
import logging


class TfgViewSet(viewsets.ModelViewSet):
    lookup_field = 'titulo'
    queryset = Tfg.objects.all()
    serializer_class = TfgSerializer
    logger = logging.getLogger(__name__)

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
            self.logger.info('INICIO WS - TFGVIEW LIST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            # if 'titulo' in params:
            #     tfg = Tfg.objects.get(titulo=params['titulo'])
            #     resul = self.serializer_class(tfg).data
            underscore = params.get('_', False) # comprobar que no se manda el parametro '_' - cosas del JQuery
            if len(params) > 0 and not underscore:
                params = utils.procesar_params_tfg(request.user, params)
                tfgs = Tfg.objects.filter(**params)
                if len(tfgs) > 0:
                    resul = utils.procesar_datos_tfgs(request.user, self.serializer_class(tfgs, many=True).data)
                else:
                    raise Tfg.DoesNotExist
            else:
                # tfg_asig = Tfg_Asig.objects.all()
                # resul = self.serializer_class(tfg_asig, many=True).data
                # if len(resul) == 0:
                #     raise NameError("No hay tfgs almacenados")
                params = utils.procesar_params_tfg(request.user, {})
                tfgs = Tfg.objects.filter(**params)
                if len(tfgs) == 0:
                    raise NameError("No hay tfgs almacenados")
                paginador = Paginator(tfgs, 20)
                pagina = params.get('pagina')
                try:
                    tfgs = paginador.page(pagina)
                    resul = {
                    'resul': utils.procesar_datos_tfgs(request.user, self.serializer_class(tfgs, many=True).data),
                    'pagina': pagina, 'num_paginas': paginador.num_pages}
                except PageNotAnInteger:
                    resul = utils.procesar_datos_tfgs(request.user, self.serializer_class(tfgs, many=True).data)
            resul_status = status.HTTP_200_OK
            self.logger.info('FIN WS - TFGVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(data=resul), status=resul_status)
        except NameError as e:
            resul = dict(message=e.message)
            self.logger.error('TFGVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Tfg.DoesNotExist:
            resul = dict(message="El tfg indicado no existe")
            self.logger.error('TFGVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un tfg nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del tfg insertado o de todos los tfgs}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TFGVIEW CREATE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('tfgs.tfg.create') or request.user.is_admin:
                # request.data['tutor'] = Profesor.objects.get(email=request.data['tutor'])
                # if 'cotutor' in request.data:
                #     request.data['cotutor'] = Profesor.objects.get(email=request.data['tutor'])
                # serializer = self.serializer_class(data=request.data)
                # if serializer.is_valid():
                #     resul = serializer.create(serializer.validated_data)
                #     if resul['status']:
                #         resul = utils.to_dict(resul)
                #         resul_status = status.HTTP_200_OK
                #     else:
                #         resul = dict(message=resul['message'])
                #         resul_status = status.HTTP_400_BAD_REQUEST
                # else:
                #     resul = dict(message=serializer.errors)
                #     resul_status = status.HTTP_400_BAD_REQUEST
                resul = Tfg.objects.create(conocimientos_previos=params.get('conocimientos_previos'),
                                           cotutor=params.get('cotutor'), descripcion=params.get('descripcion'),
                                           tutor=params.get('tutor'), hard_soft=params.get('hard_soft'),
                                           titulo=params.get('titulo'), tipo=params.get('tipo'),
                                           n_alumnos=params.get('n_alumnos'), titulacion=params.get('titulacion'))
                if resul['status']:
                    resul['data'] = self.serializer_class(resul['data']).data
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - TFGVIEW CREATE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGVIEW CREATE: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Actualizar datos de un tfg
        :param request: tfg <str>, campos <dict>
        :return :
        """

        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TFGVIEW PUT del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if (request.user.has_perm('tfgs.tfg.change') and utils.check_tfg(request.user, params.get('tfg'))) or \
                    request.user.is_admin:
                tfg = Tfg.objects.get(titulo=params.get('tfg'))
                serializer = self.serializer_class(tfg)
                params = json.loads(params['datos'])
                resul = serializer.update(tfg, params)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - TFGVIEW PUT del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Tfg.DoesNotExist:
            resul = dict(message="El tfg indicado no existe")
            self.logger.error('TFGVIEW PUT del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGVIEW PUT: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un tfg
        :param request:
        :return :
        """

        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TFGVIEW DELETE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params.get('titulo'))
                serializer = self.serializer_class(tfg)
                resul = serializer.delete_tfg(tfg)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Parametros incorrectos")
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - TFGVIEW DELETE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Tfg.DoesNotExist:
            resul = dict(message="El tfg indicado no existe")
            self.logger.error('TFGVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGVIEW DELETE: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class Tfg_asigViewSet(viewsets.ModelViewSet):
    lookup_field = 'tfg'
    queryset = Tfg_Asig.objects.all()
    serializer_class = Tfg_AsigSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de todos o de algun tfg asignado
        :param request:
        :return :
        {status: True/False, data:{serializer del tfg o tfgs}

        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TFGASIGVIEW LIST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params['titulo'])
                tfg_asig = Tfg_Asig.objects.get(tfg=tfg)
                resul = self.serializer_class(tfg_asig).data
            else:
                tfgs = Tfg_Asig.objects.all()
                if len(tfgs) == 0:
                    raise NameError("No hay tfgs almacenados")
                paginador = Paginator(tfgs, 20)
                pagina = params.get('pagina')
                try:
                    tfgs = paginador.page(pagina)
                    resul = {
                    'resul': utils.procesar_datos_tfgs_asig(request.user, self.serializer_class(tfgs, many=True).data),
                    'pagina': pagina, 'num_paginas': paginador.num_pages}
                except PageNotAnInteger:
                    resul = utils.procesar_datos_tfgs_asig(request.user, self.serializer_class(tfgs, many=True).data)
            resul_status = status.HTTP_200_OK
            self.logger.info('FIN WS - TFGVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(data=resul), status=resul_status)
        except NameError as e:
            resul = dict(message=e.message)
            self.logger.error('TFGASIGVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Tfg.DoesNotExist:
            resul = dict(message="El tfg indicado no existe")
            self.logger.error('TFGASIGVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGASIGVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Asignar un TFG a uno o varios alumnos
        :param request:
        :return:
        {status: True/False, data:{serializer del tfg asignado y de los alumnos}
        """

        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TFGASIGVIEW POST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            alumno_2 = None
            alumno_3 = None
            tfg = Tfg.objects.get(titulo=params.get('tfg'))
            alumno_1 = Alumno.objects.get(email=params.get('alumno1'))
            if 'alumno_2' in params:
                alumno_2 = Alumno.objects.get(email=params.get('alumno_2'))['id']
            if 'alumno_3' in params:
                alumno_3 = Alumno.objects.get(email=params.get('alumno_3'))['id']
            serializer = self.serializer_class(data=dict(tfg=tfg.id, alumno_1=alumno_1.id, alumno_2=alumno_2,
                                                         alumno_3=alumno_3))
            if serializer.is_valid():
                resul = serializer.create(serializer.validated_data)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message=serializer.errors)
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - TFGASIGVIEW POST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGASIGVIEW POST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TFGASIGVIEWCONVOCATORIA PUT del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('tfgs.tfg_asig.change') or request.user.is_admin:
                tfg = Tfg.objects.get(titulo=params.get('tfg'))
                tfg_asig = Tfg_Asig.objects.get(tfg=tfg)
                serializer = self.serializer_class(tfg)
                resul = serializer.update(tfg_asig, params)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Parametros incorrectos")
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - TFGASIGVIEWCONVOCATORIA PUT del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Tfg.DoesNotExist:
            resul = dict(message="El tfg indicado no existe")
            self.logger.error('TFGASIGVIEWCONVOCATORIA PUT del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGASIGVIEWCONVOCATORIA PUT: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

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
            self.logger.info('INICIO WS - TFGASIGVIEW DELETE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if 'titulo' in params:
                tfg = Tfg.objects.get(titulo=params.get('titulo'))
                tfg_asig = Tfg_Asig.objects.get(tfg=tfg)
                serializer = self.serializer_class(tfg_asig)
                resul = serializer.delete_tfg(tfg_asig)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Parametros incorrectos")
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - TFGASIGVIEW DELETE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Tfg.DoesNotExist:
            resul = dict(message="El tfg indicado no existe")
            self.logger.error('TFGASIGVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TFGASIGVIEW DELETE: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class TitulacionesViewSet(viewsets.ModelViewSet):
    lookup_field = 'codigo'
    queryset = Titulacion.objects.order_by('-created_at')
    serializer_class = TitulacionSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de las Titulaciones
        :param request:
        :return :
        {status: True/False, data:{serializer de las Titulacion}

        """
        try:
            self.logger.info('INICIO WS - TITULACIONESVIEW LIST del usuario: %s' %
                             request.user.email if hasattr(request.user, 'email') else request.user.username)
            titulaciones = Titulacion.objects.all()
            resul = self.serializer_class(titulaciones, many=True).data
            self.logger.info('FIN WS - TITULACIONESVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            self.logger.error('TITULACIONESVIEW LIST: %s' % e.message)
            return Response(dict(message=e.message), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TITULACIONESVIEW LIST del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar una titulacion nueva
        :param request:
        :return :
        {status: True/False, data:{datos de la titulacion}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TITULACIONESVIEW CREATE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            resul = Titulacion.objects.create(codigo=params.get('codigo'), nombre=params.get('nombre'))
            if resul.id:
                resul = utils.to_dict(dict(status=True, data=resul))
                resul_status = status.HTTP_200_OK
            else:
                resul = dict(message=resul['message'])
                resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.info('FIN WS - TITULACIONESVIEW CREATE del usuario: %s con params: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - TITULACIONESVIEW CREATE del usuario: %s con params: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Cambia los datos de una titulacion
        :param request:
        :return :
        {status: True/False, data:{datos de la titulacion cambiada}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TITULACIONESVIEW PUT del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('tfgs.titulacion.change') or request.user.is_admin:
                titulacion = Titulacion.objects.get(codigo=params.get('codigo'))
                params = json.loads(params.get('datos'))
                serializer = TitulacionSerializer(titulacion)
                resul = serializer.update(titulacion, params)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                resul = dict(status=False, message="Sin privilegios")
                self.logger.info('FIN WS - TITULACIONESVIEW PUT del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - TITULACIONESVIEW PUT del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar una titulacion
        :param request:
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TITULACIONESVIEW DELETE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                titulacion = Titulacion.objects.get(codigo=params.get('codigo'))
                serializer = self.serializer_class(titulacion)
                resul = serializer.delete(titulacion)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.critical('FIN WS - TITULACIONESVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul)

        except Titulacion.DoesNotExist:
            resul = dict(status=False, message="La titulacion indicada no existe")
            self.logger.error('INICIO WS - TITULACIONESVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('INICIO WS - TITULACIONESVIEW DELETE del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
