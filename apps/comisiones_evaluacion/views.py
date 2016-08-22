# -*- coding: utf-8 -*-
from comisiones_evaluacion.models import Comision_Evaluacion, Tribunales
from comisiones_evaluacion.serializers import Comision_EvaluacionSerializer, TribunalesSerializer
from authentication.models import Profesor
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status, views
from services import Comision
from tfgs.models import Tfg, Tfg_Asig
import json
import utils
import logging


class ComisionEvaluacionViewSet(viewsets.ModelViewSet):
    lookup_field = 'presidente'
    queryset = Comision_Evaluacion.objects.all()
    serializer_class = Comision_EvaluacionSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de todos o de alguna comision
        :param request:
        :return :
        {status: True/False, data:{serializer del tfg o tfgs}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - COMISIONEVALUACIONVIEW LIST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            comisiones = Comision_Evaluacion.objects.all()
            resul = self.serializer_class(comisiones, many=True).data
            if len(resul) == 0:
                raise NameError("No hay comisiones almacenadas")
            self.logger.info('FIN WS - COMISIONEVALUACIONVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            resul = dict(message=e.message)
            self.logger.error('COMISIONEVALUACIONVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Comision_Evaluacion.DoesNotExist:
            resul = dict(message="la comision indicada no existe")
            self.logger.error('COMISIONEVALUACIONVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('COMISIONEVALUACIONVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar una comision nueva
        :param request:
        :return :
        {status: True/False, data:{datos de la comision insertada o de todas las comisiones}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - COMISIONEVALUACIONVIEW POST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('comisiones_evaluacion.comision.create') or request.user.is_admin:
                comision = Comision(request.user, params.get('convocatoria'))
                resul = comision.tutores_comisiones()
                # comision.asig_tfgs()
                # while comision.reintentar:
                #     comision = Comision(request.user)
                #     resul = comision.tutores_comisiones(params.get('convocatoria'))
                #     comision.asig_tfgs()
                if resul['status']:
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - COMISIONEVALUACIONVIEW POST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('COMISIONEVALUACIONVIEW POST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Actualizar datos de una comisión
        :param request: tfg <str>, campos <dict>
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - COMISIONEVALUACIONVIEW PUT del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('comisiones_evaluacion.comision.change') or request.user.is_admin:
                presidente = Profesor.objects.get(email=params.get('presidente'))
                comision = Comision_Evaluacion.objects.get(presidente=presidente)
                serializer = self.serializer_class(comision)
                params = json.loads(params.get('datos'))
                resul = serializer.update(request.user, comision, params)
                if resul['status']:
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Parametros incorrectos")
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - COMISIONEVALUACIONVIEW PUT del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Profesor.DoesNotExist:
            resul = dict(message="El presidente de la comision no existe")
            self.logger.error('COMISIONEVALUACIONVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('COMISIONEVALUACIONVIEW PUT: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar una comisión
        :param request:
        :return :
        """

        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - COMISIONEVALUACIONVIEW DELETE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if 'titulo' in params:
                comision = Comision_Evaluacion.objects.get(presidente=params.get('presidente'))
                serializer = self.serializer_class(comision)
                resul = serializer.delete_tfg(comision)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Parametros incorrectos")
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - COMISIONEVALUACIONVIEW DELETE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Comision_Evaluacion.DoesNotExist:
            resul = dict(message="La comision indicada no existe")
            self.logger.error('COMISIONEVALUACIONVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('COMISIONEVALUACIONVIEW DELETE: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class TribunalesViewSet(viewsets.ModelViewSet):
    lookup_field = 'tfg'
    queryset = Tribunales.objects.all()
    serializer_class = TribunalesSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de todos o de algun tribunal
        :param request:
        :return :
        {status: True/False, data:{serializer del tfg o tfgs}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TRIBUNALESNVIEW LIST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            tribunales = Tribunales.objects.all()
            resul = utils.procesar_datos_tribunales(request.user, self.serializer_class(tribunales, many=True).data)
            if len(resul) == 0:
                raise NameError("No hay tribunales almacenados")
            self.logger.info('FIN WS - TRIBUNALESNVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            resul = dict(message=e.message)
            self.logger.error('TRIBUNALESNVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Tribunales.DoesNotExist:
            resul = dict(message="El tribunal indicado no existe")
            self.logger.error('TRIBUNALESNVIEW LIST del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TRIBUNALESNVIEW LIST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar los tribunales a partir de una comision
        :param request:
        :return :
        {status: True/False, data:{datos de la comision insertada o de todas las comisiones}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - COMISIONEVALUACIONVIEW POST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('comisiones_evaluacion.comision.create') or request.user.is_admin:
                comisiones = utils.to_bool(params.get('comisiones'))
                convocatoria = params.get('convocatoria')
                comision = Comision(request.user, convocatoria, comisiones=comisiones)
                resul = comision.asig_tfgs()
                while comision.reintentar:
                    comision = Comision(request.user, convocatoria, comisiones=comisiones)
                    comision.asig_tfgs()
                if resul['status']:
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - COMISIONEVALUACIONVIEW POST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('COMISIONEVALUACIONVIEW POST: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Actualizar datos de un tribunal
        :param request: tfg <str>, campos <dict>
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - TRIBUNALESNVIEW PUT del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('tribunales.tribunal.change') or request.user.is_admin:
                tfg = Tfg.objects.get(titulo=params.get('tfg'))
                tfg_asig = Tfg_Asig.objects.get(tfg=tfg)
                tribunal = Tribunales.objects.get(tfg=tfg_asig)
                serializer = self.serializer_class(tribunal)
                params = json.loads(params.get('datos'))
                resul = serializer.update(tribunal, params)
                if resul['status']:
                    resul['data'] = utils.procesar_datos_tribunales(request.user, resul['data'])[0]
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message=resul['message'])
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Parametros incorrectos")
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - TRIBUNALESNVIEW PUT del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('TRIBUNALESNVIEW PUT: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
