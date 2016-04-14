from django.contrib.auth import authenticate, login, logout
from authentication.models import Alumno, Profesor
from authentication.serializers import AlumnoSerializer, ProfesorSerializer, UsuarioSerializer
from rest_framework import permissions, viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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

        # TODO: Aqui va la comprobacion del perfil del usuario

        # Si es un GET, devuelvo la info de todos los alumnos
        try:
            params = utils.get_params(request)
            try:
                if 'email' in params:
                    alumno = Alumno.objects.get(email=params['email'])
                    resul = AlumnoSerializer(alumno).data
                elif request.user.has_perm('authentication.alumns_can_get_all'):
                    alumno = Alumno.objects.all()
                    resul = AlumnoSerializer(alumno, many=True).data
                    if len(resul) == 0:
                        raise NameError("No hay alumnos almacenados")
                else:
                    return Response(dict(status=False, message="No tienes los permisos necesarios"))

                return Response(dict(status=True, data=resul))
            except NameError as e:
                return Response(dict(status=False, message=e.message))
            except Alumno.DoesNotExist:
                return Response(dict(status=False, message="El alumno indicado no existe"))

        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"))

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
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                resul = Alumno.objects.create_user(**serializer.validated_data)
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
        Insertar un alumno nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del alumno insertado o de todos los alumnos}

        :param request:
        :return:
        """
        try:
            alumno = Alumno.objects.get(email=request.data['alumno'])
            params = json.loads(request.data['datos'])
            serializer = AlumnoSerializer(alumno)
            resul = serializer.update(alumno, params)
            if resul['status']:
                return Response(utils.to_dict(resul))
            else:
                return Response(resul)
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)


class ProfesoresViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

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

        # TODO: Aqui va la comprobacion del perfil del usuario

        # Si es un GET, devuelvo la info de todos los alumnos
        try:
            params = utils.get_params(request)
            try:
                if 'email' in params:
                    profesor = Profesor.objects.get(email=params['email'])
                    resul = ProfesorSerializer(profesor).data
                elif request.user.has_perm('authentication.profesores_can_get_all') or request.user.is_admin:
                    profesores = Profesor.objects.all()
                    resul = ProfesorSerializer(profesores, many=True).data
                    if len(resul) == 0:
                        raise NameError("No hay profesores almacenados")
                else:
                    return Response(dict(status=False, message="No tienes los permisos necesarios"))

                return Response(utils.to_dict(dict(status=True, data=json.dumps(resul))))
            except NameError as e:
                return Response(dict(status=False, message=e.message))
            except Profesor.DoesNotExist:
                return  Response(dict(status=False, message="El profesor indicado no existe"))

        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"))

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
            serializer = self.serializer_class(data=request.data)
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
        Insertar un alumno nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del alumno insertado o de todos los alumnos}

        :param request:
        :return:
        """
        try:
            profesor = Profesor.objects.get(email=request.data['profesor'])
            params = json.loads(request.data['datos'])
            serializer = ProfesorSerializer(profesor)
            resul = serializer.update(profesor, params)
            if resul['status']:
                return Response(utils.to_dict(resul))
            else:
                return Response(resul)
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"), status=status.HTTP_400_BAD_REQUEST)


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
                if isinstance(account, Alumno):
                    serialized = AlumnoSerializer(account)
                elif isinstance(account, Profesor):
                    serialized = ProfesorSerializer(account)
                else:
                    serialized = UsuarioSerializer(account)
                return Response(serialized.data)
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
