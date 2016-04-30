# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from authentication.models import Alumno, Profesor
from authentication.serializers import AlumnoSerializer, ProfesorSerializer, UsuarioSerializer
from rest_framework import permissions, viewsets, status, views
from rest_framework.response import Response
from django.contrib.auth.models import Permission
import json
import utils


class AlumnosViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #
    #     if self.request.method == 'POST':
    #         return (permissions.AllowAny(),)
    #
    #     return (permissions.IsAuthenticated(), IsAccountOwner(),)

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
                else:
                    alumno = Alumno.objects.all()
                    resul = self.serializer_class(alumno, many=True).data
                    if len(resul) == 0:
                        raise NameError("No hay alumnos almacenados")

                return Response(dict(status=True, data=json.dumps(resul)))
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
            if utils.check_usuario(request.user, params['alumno']):
                alumno = Alumno.objects.get(email=params['alumno'])
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
            if 'email' in params and utils.check_usuario(request.user):
                alumno = Alumno.objects.get(email=params['email'])
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
                    profesor = Profesor.objects.get(email=params['email'])
                    resul = ProfesorSerializer(profesor).data
                else:
                    profesores = Profesor.objects.all()
                    resul = ProfesorSerializer(profesores, many=True).data
                    if len(resul) == 0:
                        raise NameError("No hay profesores almacenados")

                return Response(dict(status=True, data=json.dumps(resul)))
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
        {status: True/False, data:{datos del profesor insertado o de todos los profesores}

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
            if utils.check_usuario(request.user, params['profesor']):
                profesor = Profesor.objects.get(email=params['profesor'])
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
            if 'email' in params and utils.check_usuario(request.user):
                profesor = Profesor.objects.get(email=params['email'])
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

    def post(self, request, format=None):
        # params = utils.get_params(request)
        params = request.data

        email = params.get('email', None)
        password = params.get('password', None)

        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)
                if hasattr(account, 'alumno') and isinstance(account.alumno, Alumno):
                    serialized = AlumnoSerializer(account.alumno)
                elif hasattr(account, 'profesor') and isinstance(account.profesor, Profesor):
                    serialized = ProfesorSerializer(account.profesor)
                else:
                    serialized = UsuarioSerializer(account)
                permissions = Permission.objects.filter(group=serialized.instance.groups.all()).values('codename')
                list_permissions = []
                for permission in permissions:
                    list_permissions.append(permission['codename'])
                return Response(dict(data=serialized.data, permissions=list_permissions))
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class PermissionsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        permissions = Permission.objects.filter(group=request.user.groups.all()).values('codename')
        list_permissions = []
        for permission in permissions:
            list_permissions.append(permission['codename'])
        return Response(dict(permissions=list_permissions))

    # TODO el POST sera para cambiar de grupo a un usuario
