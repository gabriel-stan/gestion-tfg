# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from authentication.models import Alumno, Profesor, Grupos, Usuario, Departamento
from authentication.serializers import AlumnoSerializer, ProfesorSerializer, UsuarioSerializer, DepartamentoSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import permissions, viewsets, status, views
from rest_framework.response import Response
from django.contrib.auth.models import Permission
import json
import utils
import django.apps
import logging


class UsuariosViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de todos los usuarios
        :param request:
        :return :
        {status: True/False, data:{serializer del alumno o alumnos}
        """

        # Si es un GET, devuelvo la info de todos los alumnos
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - USUARIOSVIEW LIST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('tfgs.tfg.create') or request.user.is_admin:
                try:
                    if 'email' in params:
                        usuario = Usuario.objects.get(email=params['email'])
                        datas = utils.procesar_datos_usuario(request.user, self.serializer_class(usuario).data)
                    elif 'dni' in params:
                        usuario = Usuario.objects.get(dni=params['dni'])
                        datas = utils.procesar_datos_usuario(request.user, self.serializer_class(usuario).data)
                    else:
                        usuarios = Usuario.objects.all()
                        if len(usuarios) == 0:
                            raise NameError("No hay usuarios almacenados")
                        paginador = Paginator(usuarios, 20)
                        pagina = params.get('pagina')
                        try:
                            usuarios = paginador.page(pagina)
                        except PageNotAnInteger:
                            pagina = 1
                            usuarios = paginador.page(pagina)
                        except EmptyPage:
                            pagina = paginador.num_pages
                            usuarios = paginador.page(pagina)
                        datas = {'resul': utils.procesar_datos_usuario(request.user,
                                                                       self.serializer_class(usuarios, many=True).data),
                                 'pagina': pagina, 'num_paginas': paginador.num_pages}
                    resul = dict(status=True, data=datas)
                    resul_status = status.HTTP_200_OK
                    
                except NameError as e:
                    resul = dict(status=False, message=e.message)
                    resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
                except Usuario.DoesNotExist:
                    resul = dict(status=False, message="El usuario indicado no existe")
                    resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            else:
                resul = dict(status=False, message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - USUARIOSVIEW LIST del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('USUARIOSVIEW LIST: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un usuario nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del alumno insertado o de todos los alumnos}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - USUARIOSVIEW CREATE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                is_admin = str(params.get('is_admin'))
                serializer = self.serializer_class(data=params)
                if serializer.is_valid():
                    if is_admin and is_admin == 'True':
                        resul = Usuario.objects.create_superuser(**serializer.validated_data)
                    else:
                        resul = Usuario.objects.create_user(**serializer.validated_data)
                    if resul['status']:
                        resul = utils.to_dict(resul)
                        resul_status = status.HTTP_200_OK
                    else:
                        resul_status = status.HTTP_400_BAD_REQUEST
                else:
                    resul = dict(status=False, message=serializer.errors)
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - USUARIOSVIEW CREATE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('USUARIOSVIEW CREATE: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Modificar los datos de un alumno
        :param request:
        :return :
        {status: True/False, data:{datos del alumno}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - USUARIOSSVIEW PUT del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if utils.check_usuario(request.user, params['usuario']):
                if utils.is_email(params['usuario']):
                    usuario = Usuario.objects.get(email=params['usuario'])
                elif utils.is_dni(params['usuario']):
                    usuario = Usuario.objects.get(dni=params['usuario'])
                params = json.loads(request.data['datos'])
                serializer = self.serializer_class(usuario)
                resul = serializer.update(usuario, params)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(status=False, message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - USUARIOSSVIEW PUT del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('USUARIOSSVIEW PUT: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class AlumnosViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de todos o de algun alumno
        :param request:
        :return :
        {status: True/False, data:{serializer del alumno o alumnos}
        """

        # Si es un GET, devuelvo la info de todos los alumnos
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - ALUMNOSVIEW LIST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            try:
                if 'email' in params:
                    alumno = Alumno.objects.get(email=params['email'])
                    datas = self.serializer_class(alumno).data
                elif 'dni' in params:
                    alumno = Alumno.objects.get(dni=params['dni'])
                    datas = self.serializer_class(alumno).data
                else:
                    alumnos = Alumno.objects.all()
                    if len(alumnos) == 0:
                        raise NameError("No hay alumnos almacenados")
                    paginador = Paginator(alumnos, 20)
                    pagina = params.get('pagina')

                    try:
                        alumnos = paginador.page(pagina)
                    except PageNotAnInteger:
                        pagina = 1
                        alumnos = paginador.page(pagina)
                    except EmptyPage:
                        pagina = paginador.num_pages
                        alumnos = paginador.page(pagina)
                    datas = {'resul': utils.procesar_datos_usuario(request.user, self.serializer_class(alumnos,
                                                                                                       many=True).data),
                             'pagina': pagina, 'num_paginas': paginador.num_pages}
                resul = dict(status=True, data=datas)
                resul_status = status.HTTP_200_OK
                self.logger.info('FIN WS - ALUMNOSVIEW LIST del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=resul_status)
            except NameError as e:
                resul = dict(status=False, message=e.message)
                resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.error('FIN WS - ALUMNOSVIEW LIST del usuario: %s con resultado: %s' %
                                  (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                   resul))
                return Response(resul, status=resul_status)
            except Alumno.DoesNotExist:
                resul = dict(status=False, message="El alumno indicado no existe")
                resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.error('FIN WS - ALUMNOSVIEW LIST del usuario: %s con resultado: %s' %
                                  (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                   resul))
                return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('ALUMNOSVIEW LIST: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un alumno nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del alumno insertado o de todos los alumnos}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - ALUMNOSVIEW CREATE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            serializer = self.serializer_class(data=params)
            if serializer.is_valid():
                resul = Alumno.objects.create_user(**serializer.validated_data)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.info('FIN WS - ALUMNOSVIEW CREATE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=resul_status)
            else:
                resul = dict(status=False, message=serializer.errors)
                self.logger.info('FIN WS - ALUMNOSVIEW CREATE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
                return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('ALUMNOSVIEW CREATE: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Modificar los datos de un alumno
        :param request:
        :return :
        {status: True/False, data:{datos del alumno}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - ALUMNOSVIEW PUT del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if utils.check_usuario(request.user, params['usuario']):
                if utils.is_email(params['usuario']):
                    alumno = Alumno.objects.get(email=params['usuario'])
                elif utils.is_dni(params['usuario']):
                    alumno = Alumno.objects.get(dni=params['usuario'])
                params = json.loads(request.data['datos'])
                serializer = self.serializer_class(alumno)
                resul = serializer.update(alumno, params)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(status=False, message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            self.logger.info('FIN WS - ALUMNOSVIEW PUT del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('ALUMNOSVIEW PUT: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un alumno
        :param request:
        :return :
        """

        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - ALUMNOSVIEW DELETE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                if utils.is_email(params.get('email')):
                    alumno = Alumno.objects.get(email=params.get('email'))
                elif utils.is_dni(params.get('dni')):
                    alumno = Alumno.objects.get(dni=params.get('dni'))
                serializer = self.serializer_class(alumno)
                resul = serializer.delete(alumno)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.info('FIN WS - ALUMNOSVIEW DELETE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_200_OK)
        except Profesor.DoesNotExist:
            resul = (dict(status=False, message="El alumno indicado no existe"))
            self.logger.error('FIN WS - ALUMNOSVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('ALUMNOSVIEW DELETE: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class ProfesoresViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de todos o de algun profesor
        :param request:
        :return :
        {status: True/False, data:{serializer del profesor o profesores}
        """
        # Si es un GET, devuelvo la info de todos los alumnos
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - PROFESORVIEW LIST del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            try:
                if 'email' in params:
                    profesor = Profesor.objects.get(email=params['email'])
                    datas = self.serializer_class(profesor).data
                elif 'dni' in params:
                    profesor = Profesor.objects.get(dni=params['dni'])
                    datas = self.serializer_class(profesor).data
                else:
                    profesores = Profesor.objects.all()
                    if len(profesores) == 0:
                        raise NameError("No hay profesores almacenados")
                    paginador = Paginator(profesores, 20)
                    pagina = params.get('pagina')
                    try:
                        profesores = paginador.page(pagina)
                    except PageNotAnInteger:
                        pagina = 1
                        profesores = paginador.page(pagina)
                    except EmptyPage:
                        pagina = paginador.num_pages
                        profesores = paginador.page(pagina)
                    datas = {'resul': utils.procesar_datos_usuario(request.user, self.serializer_class(profesores,
                                                                                                       many=True).data),
                             'pagina': pagina, 'num_paginas': paginador.num_pages}
                return Response(dict(status=True, data=datas), status=status.HTTP_200_OK)
            except NameError as e:
                resul = dict(status=False, message=e.message)
                self.logger.error('FIN WS - PROFESORVIEW LIST del usuario: %s con resultado: %s' %
                                  (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                   resul))
                return Response(resul, status=status.HTTP_400_BAD_REQUEST)
            except Profesor.DoesNotExist:
                resul = dict(status=False, message="El profesor indicado no existe")
                self.logger.error('FIN WS - PROFESORVIEW LIST del usuario: %s con resultado: %s' %
                                  (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                   resul))
                return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('PROFESORVIEW LIST: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un profesor nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del profesor insertado}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - PROFESORVIEW CREATE del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            params['departamento'] = Departamento.objects.get(codigo=params['departamento']).id
            #resul = Profesor.objects.create_user(**params)
            serializer = self.serializer_class(data=params)
            if serializer.is_valid():
                resul = Profesor.objects.create_user(**serializer.validated_data)
                if resul['status']:
                    resul = utils.to_dict(resul)
                    resul_status = status.HTTP_200_OK
                else:
                    resul_status = status.HTTP_400_BAD_REQUEST
            else:
                resul = dict(status=False, message=serializer.errors)
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - PROFESORVIEW CREATE del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('PROFESORVIEW CREATE: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Cambia los datos de un profesor
        :param request:
        :return :
        {status: True/False, data:{datos del profesor cambiado}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - PROFESORVIEW PUT del usuario: %s con parametros: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if utils.check_usuario(request.user, params['usuario']):
                if utils.is_email(params['usuario']):
                    profesor = Profesor.objects.get(email=params['usuario'])
                elif utils.is_dni(params['usuario']):
                    profesor = Profesor.objects.get(dni=params['usuario'])
                params = json.loads(params['datos'])
                serializer = ProfesorSerializer(profesor)
                resul = serializer.update(profesor, params)
            else:
                resul = dict(status=False, message="Sin privilegios")
            if resul['status']:
                resul = utils.to_dict(resul)
                resul_status = status.HTTP_200_OK
            else:
                resul_status = status.HTTP_400_BAD_REQUEST
            self.logger.info('FIN WS - PROFESORVIEW PUT del usuario: %s con resultado: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('PROFESORVIEW PUT: %s %s' % (resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un profesor
        :param request:
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - PROFESORVIEW DELETE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                if utils.is_email(params.get('email')):
                    profesor = Profesor.objects.get(email=params.get('email'))
                elif utils.is_dni(params.get('dni')):
                    profesor = Profesor.objects.get(dni=params.get('dni'))
                serializer = self.serializer_class(profesor)
                resul = serializer.delete(profesor)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.info('FIN WS - PROFESORVIEW DELETE: con resultado: %s' % resul)
            return Response(resul)

        except Profesor.DoesNotExist:
            resul = dict(status=False, message="El profesor indicado no existe")
            self.logger.error('PROFESORVIEW DELETE: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('PROFESORVIEW DELETE: %s' % resul)
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    lookup_field = 'email'
    queryset = Usuario.objects.all()
    logger = logging.getLogger(__name__)

    def post(self, request, format=None):

        try:
            # params = utils.get_params(request)
            params = request.data

            email = params.get('email')
            dni = params.get('dni')
            password = params.get('password')

            if email:
                self.logger.info('INICIO WS - LOGINVIEW del usuario: %s' % params.get('email'))
                user = Usuario.objects.get(email=params['email'])
            elif dni:
                self.logger.info('INICIO WS - LOGINVIEW del usuario: %s' % params.get('dni'))
                user = Usuario.objects.get(dni=params['dni'])
            else:
                self.logger.error('LOGINVIEW: Es necesario un dni o email validos')
                raise NameError("Es necesario un dni o email validos")
            account = authenticate(id=user.id, password=password)

            if account is not None:
                if account.is_active:
                    login(request, account)
                    if hasattr(account, 'alumno') and isinstance(account.alumno, Alumno):
                        serialized = AlumnoSerializer(account.alumno)
                    elif hasattr(account, 'profesor') and isinstance(account.profesor, Profesor):
                        serialized = ProfesorSerializer(account.profesor)
                    else:
                        serialized = UsuarioSerializer(account)
                    # permissions = Permission.objects.filter(group=serialized.instance.groups.all()).values('codename')
                    # list_permissions = []
                    # for permission in permissions:
                    #     list_permissions.append(permission['codename'])
                    list_permissions = utils.permisos(request.user)
                    resul = dict(data=serialized.data, permissions=list_permissions)
                    resul_status = status.HTTP_200_OK
                else:
                    resul = dict(message='La cuenta esta deshabilitada')
                    resul_status = status.HTTP_401_UNAUTHORIZED
            else:
                resul = dict(message='Usuario/Clave incorrectos.')
                resul_status = status.HTTP_401_UNAUTHORIZED
            self.logger.info('FIN WS - LOGINVIEW: con resultado: %s' % resul)
            return Response(resul, status=resul_status)
        except NameError as e:
                self.logger.error('LOGINVIEW: %s' % e.message)
                return Response(dict(status=False, message=e.message), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.critical('LOGINVIEW: %s' % e.message)
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    logger = logging.getLogger(__name__)

    def post(self, request):
        self.logger.info('INICIO WS - LOGOUTVIEW del usuario: %s' %
                         request.user.email if hasattr(request.user, 'email') else request.user.username)
        logout(request)
        self.logger.info('FIN WS - LOGOUTVIEW del usuario: %s' %
                         request.user.email if hasattr(request.user, 'email') else request.user.username)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class PermissionsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    logger = logging.getLogger(__name__)

    def get(self, request):
        self.logger.info('INICIO WS - PERMISSIONSVIEW GET del usuario: %s' %
                         request.user.email if hasattr(request.user, 'email') else request.user.username)
        grupos = Grupos.objects.filter(user=request.user)
        list_permissions = utils.permisos(request.user)
        list_grupos = utils.grupos(grupos)
        resul = dict(grupos=list_grupos, permissions=list_permissions)
        self.logger.info('FIN WS - PERMISSIONSVIEW GET del usuario: %s, con resultado: %s' %
                         (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
        return Response(resul, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            self.logger.info('INICIO WS - PERMISSIONSVIEW POST del usuario: %s' %
                             request.user.email if hasattr(request.user, 'email') else request.user.username)
            if request.user.is_admin:
                params = utils.get_params(request)
                grupo = Grupos.objects.get(user=request.user)
                nuevo_grupo = Grupos.objects.get(name=params.get('grupo', None))
                grupo.user_set.remove(request.user)
                nuevo_grupo.user_set.add(request.user)
                resul = dict(message="OK")
                resul_status = status.HTTP_200_OK
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
                self.logger.info('FIN WS - PERMISSIONSVIEW POST del usuario: %s, con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            self.logger.critical('PERMISSIONSVIEW POST: %s' % e.message)
            return Response(dict(message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)


class LoadDataView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    logger = logging.getLogger(__name__)

    def post(self, request):
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - LOADDATAVIEW POST del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                models = django.apps.apps.get_models()
                file = request.FILES['file']
                model = params.get('model')
                for i in models:
                    if i._meta.model_name == model:
                        resul = self.load_data(i, file)
                        break
                if resul['status']:
                    resul_status = status.HTTP_200_OK
                else:
                    resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.info('FIN WS - LOADDATAVIEW POST del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            else:
                resul = dict(message="Sin privilegios")
                self.logger.error('FIN WS - LOADDATAVIEW POST del usuario: %s con resultado: %s' %
                                  (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                   resul))
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(message="Error en la llamada")
            self.logger.critical(('LOADDATAVIEW POST: %s %s' % (resul, e)))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def load_data(self, model, file):
        errores = []
        columnas = file.readline().rstrip().split(';')
        file = file.readlines()
        for linea in file:
            linea = linea.rstrip().split(';')
            datos = {}
            for key, value in enumerate(columnas):
                datos[value] = linea[key]
            model.objects.create_file(**datos)
        return dict(status=True, data=errores)


class DepartamentosViewSet(viewsets.ModelViewSet):
    lookup_field = 'codigo'
    queryset = Departamento.objects.order_by('-created_at')
    serializer_class = DepartamentoSerializer
    logger = logging.getLogger(__name__)

    def list(self, request):
        """
        GET
        Obtener los datos de los departamentos
        :param request:
        :return :
        {status: True/False, data:{serializer de los departamentos}

        """
        try:
            self.logger.info('INICIO WS - DEPARTAMENTOSVIEW LIST del usuario: %s' %
                             request.user.email if hasattr(request.user, 'email') else request.user.username)
            departamentos = Departamento.objects.all()
            utils.procesar_datos_departamento(departamentos)
            resul = self.serializer_class(departamentos, many=True).data
            self.logger.info('FIN WS - DEPARTAMENTOSVIEW LIST del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(dict(data=resul), status=status.HTTP_200_OK)
        except NameError as e:
            self.logger.error('DEPARTAMENTOSVIEW LIST: %s' % e.message)
            return Response(dict(message=e.message), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('DEPARTAMENTOSVIEW LIST del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST
        Insertar un departamento nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del departamento}
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - DEPARTAMENTOSVIEW CREATE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            resul = Departamento.objects.create(codigo=params.get('codigo'), nombre=params.get('nombre'))
            if resul.id:
                resul = utils.to_dict(dict(status=True, data=resul))
                resul_status = status.HTTP_200_OK
            else:
                resul = dict(message=resul['message'])
                resul_status = status.HTTP_400_BAD_REQUEST
                self.logger.info('FIN WS - DEPARTAMENTOSVIEW CREATE del usuario: %s con params: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul, status=resul_status)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('FIN WS - DEPARTAMENTOSVIEW CREATE del usuario: %s con params: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        PUT
        Cambia los datos de un departamento
        :param request:
        :return :
        {status: True/False, data:{datos del departamento cambiado}

        :param request:
        :return:
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - DEPARTAMENTOSVIEW PUT del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.has_perm('authentication.departemento.change') or request.user.is_admin:
                departamento = Departamento.objects.get(codigo=params.get('codigo'))
                params = json.loads(params.get('data'))
                serializer = DepartamentoSerializer(departamento)
                resul = serializer.update(departamento, params)
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
            self.logger.critical('FIN WS - DEPARTAMENTOSVIEW PUT del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Eliminar un departamento
        :param request:
        :return :
        """
        try:
            params = utils.get_params(request)
            self.logger.info('INICIO WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con params: %s' %
                             (request.user.email if hasattr(request.user, 'email') else request.user.username, params))
            if request.user.is_admin:
                departamento = Departamento.objects.get(codigo=params.get('codigo'))
                serializer = self.serializer_class(departamento)
                resul = serializer.delete(departamento)
            else:
                resul = dict(status=False, message="Parametros incorrectos")
            self.logger.critical('FIN WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul))
            return Response(resul)

        except Profesor.DoesNotExist:
            resul = dict(status=False, message="El departamento indicado no existe")
            self.logger.error('INICIO WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con resultado: %s' %
                              (request.user.email if hasattr(request.user, 'email') else request.user.username, resul))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            resul = dict(status=False, message="Error en la llamada")
            self.logger.critical('INICIO WS - DEPARTAMENTOSVIEW DELETE del usuario: %s con resultado: %s %s' %
                                 (request.user.email if hasattr(request.user, 'email') else request.user.username,
                                  resul, e))
            return Response(resul, status=status.HTTP_400_BAD_REQUEST)
