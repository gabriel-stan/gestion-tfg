# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from authentication.models import Alumno, Profesor, Grupos, Usuario
from authentication.serializers import AlumnoSerializer, ProfesorSerializer, UsuarioSerializer
from rest_framework import permissions, viewsets, status, views
from rest_framework.response import Response
from django.contrib.auth.models import Permission
import json
import utils


class UsuariosViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

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
            if request.user.is_admin:
                params = utils.get_params(request)
                try:
                    if 'email' in params:
                        usuario = Usuario.objects.get(email=params['email'])
                        resul = self.serializer_class(usuario).data
                    elif 'dni' in params:
                        usuario = Usuario.objects.get(dni=params['dni'])
                        resul = self.serializer_class(usuario).data
                    else:
                        usuario = Usuario.objects.all()
                        resul = self.serializer_class(usuario, many=True).data
                        if len(resul) == 0:
                            raise NameError("No hay usuarios almacenados")
                    return Response(dict(status=True, data=resul))
                except NameError as e:
                    return Response(dict(status=False, message=e.message))
                except Usuario.DoesNotExist:
                    return Response(dict(status=False, message="El usuario indicado no existe"))
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            return Response(resul, status=resul_status)
        except Exception as e:
            return Response(dict(message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

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
            if request.user.is_admin:
                params = utils.get_params(request)
                is_admin = str(params.get('is_admin', None))
                serializer = self.serializer_class(data=params)
                if serializer.is_valid():
                    if is_admin and is_admin == 'True':
                        resul = Usuario.objects.create_superuser(**serializer.validated_data)
                    else:
                        resul = Usuario.objects.create_user(**serializer.validated_data)
                    if resul['status']:
                        return Response(utils.to_dict(resul))
                    else:
                        return Response(resul, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(dict(status=False, message=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                resul = dict(message="Sin privilegios")
                resul_status = status.HTTP_405_METHOD_NOT_ALLOWED
            return Response(resul, status=resul_status)
        except Exception as e:
            return Response(dict(message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)


class AlumnosViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

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
            try:
                if 'email' in params:
                    alumno = Alumno.objects.get(email=params['email'])
                    resul = self.serializer_class(alumno).data
                elif 'dni' in params:
                    alumno = Alumno.objects.get(dni=params['dni'])
                    resul = self.serializer_class(alumno).data
                else:
                    alumno = Alumno.objects.all()
                    resul = self.serializer_class(alumno, many=True).data
                    if len(resul) == 0:
                        raise NameError("No hay alumnos almacenados")

                return Response(dict(status=True, data=resul))
            except NameError as e:
                return Response(dict(status=False, message=e.message))
            except Alumno.DoesNotExist:
                return Response(dict(status=False, message="El alumno indicado no existe"))

        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

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
            serializer = self.serializer_class(data=params)
            if serializer.is_valid():
                resul = Alumno.objects.create_user(**serializer.validated_data)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(dict(status=False, message=serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

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
            if utils.check_usuario(request.user, params['usuario']):
                if utils.is_email(params['usuario']):
                    alumno = Alumno.objects.get(email=params['usuario'])
                elif utils.is_dni(params['usuario']):
                    alumno = Alumno.objects.get(dni=params['usuario'])
                params = json.loads(request.data['datos'])
                serializer = self.serializer_class(alumno)
                resul = serializer.update(alumno, params)
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
        Eliminar un alumno
        :param request:
        :return :
        """

        try:
            params = utils.get_params(request)
            if request.user.is_admin:
                if utils.is_email(params.get('email')):
                    alumno = Alumno.objects.get(email=params.get('email'))
                elif utils.is_dni(params.get('dni')):
                    alumno = Alumno.objects.get(dni=params.get('dni'))
                serializer = self.serializer_class(alumno)
                resul = serializer.delete(alumno)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

        except Profesor.DoesNotExist:
            return Response(dict(status=False, message="El alumno indicado no existe"))
        except Exception:
            return Response(dict(status=False, message="Error en la llamada"))


class ProfesoresViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

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
            try:
                if 'email' in params:
                    profesor = Profesor.objects.get(email=params['email'])
                    resul = self.serializer_class(profesor).data
                elif 'dni' in params:
                    profesor = Profesor.objects.get(dni=params['dni'])
                    resul = self.serializer_class(profesor).data
                else:
                    profesores = Profesor.objects.all()
                    resul = ProfesorSerializer(profesores, many=True).data
                    if len(resul) == 0:
                        raise NameError("No hay profesores almacenados")
                return Response(dict(status=True, data=resul))
            except NameError as e:
                return Response(dict(status=False, message=e.message))
            except Profesor.DoesNotExist:
                return Response(dict(status=False, message="El profesor indicado no existe"))
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

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
            serializer = self.serializer_class(data=params)
            if serializer.is_valid():
                resul = Profesor.objects.create_user(**serializer.validated_data)
                if resul['status']:
                    return Response(utils.to_dict(resul))
                else:
                    return Response(resul)
            else:
                return Response(dict(status=False, message=serializer.errors), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)

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
            if utils.check_usuario(request.user, params['usuario']):
                if utils.is_email(params['usuario']):
                    profesor = Profesor.objects.get(email=params['usuario'])
                elif utils.is_dni(params['usuario']):
                    profesor = Profesor.objects.get(dni=params['usuario'])
                params = json.loads(params['datos'])
                serializer = ProfesorSerializer(profesor)
                resul = serializer.update(profesor, params)
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
        Eliminar un profesor
        :param request:
        :return :
        """
        try:
            params = utils.get_params(request)
            if request.user.is_admin:
                if utils.is_email(params.get('email')):
                    profesor = Profesor.objects.get(email=params.get('email'))
                elif utils.is_dni(params.get('dni')):
                    profesor = Profesor.objects.get(dni=params.get('dni'))
                serializer = self.serializer_class(profesor)
                resul = serializer.delete(profesor)
            else:
                resul = dict(status=False, message="Parametros incorrectos")

            return Response(resul)

        except Profesor.DoesNotExist:
            return Response(dict(status=False, message="El profesor indicado no existe"))
        except Exception:
            return Response(dict(status=False, message="Error en la llamada"))


class LoginView(views.APIView):
    lookup_field = 'email'
    queryset = Usuario.objects.all()

    def post(self, request, format=None):

        try:
            # params = utils.get_params(request)
            params = request.data

            email = params.get('email', None)
            dni = params.get('dni', None)
            password = params.get('password', None)

            if email:
                user = Usuario.objects.get(email=params['email'])
            elif dni:
                user = Usuario.objects.get(dni=params['dni'])
            else:
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
                    resul = dict(message='This account has been disabled.')
                    resul_status = status.HTTP_401_UNAUTHORIZED
            else:
                resul = dict(message='Usuario/Clave incorrectos.')
                resul_status = status.HTTP_401_UNAUTHORIZED
            return Response(resul, status=resul_status)
        except NameError as e:
                return Response(dict(status=False, message=e.message))
        except Exception:
            return Response(dict(status=False, message="Error en la llamada"))


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class PermissionsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        grupo = Grupos.objects.get(user=request.user)
        list_permissions = utils.permisos(request.user)
        return Response(dict(grupo=grupo.name, code=grupo.code, permissions=list_permissions))

    def post(self, request, format=None):
        try:
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
            return Response(resul, status=resul_status)
        except Exception as e:
            return Response(dict(message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)
