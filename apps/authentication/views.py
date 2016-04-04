import utils
from rest_framework import permissions, viewsets
from authentication.models import Alumno
from authentication.serializers import AlumnoSerializer
from rest_framework.response import Response


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

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            resul = Alumno.objects.create_user(**serializer.validated_data)

            return Response(utils.to_dict(resul))

        Response(dict(status=False, message="Error en la llamada"))

    def alumnos(self, request):
        """
        GET
        Obtener los datos de todos o de algun alumno
        :param request:
        :return :
        {status: True/False, data:{serializer del alumno o alumnos}

        POST
        Insertar un alumno nuevo
        :param request:
        :return :
        {status: True/False, data:{datos del alumno insertado o de todos los alumnos}
        """

        # TODO: Aqui va la comprobacion del perfil del usuario

        # Si es un GET, devuelvo la info de todos los alumnos
        try:
            if request.method == 'GET':
                params = utils.get_params(request)
                try:
                    if 'email' in params:
                        alumno = Alumno.objects.get(username=params['email'])
                        resul = AlumnoSerializer(alumno).data
                    else:
                        alumno = Alumno.objects.all()
                        resul = AlumnoSerializer(alumno, many=True).data
                        if len(resul) == 0:
                            raise NameError("No hay alumnos almacenados")

                    return Response(utils.to_dict(dict(status=True, data=resul)))
                except NameError as e:
                    return dict(status=False, message=e.message)
                except Alumno.DoesNotExist:
                    return dict(status=False, message="El alumno indicado no existe")

            # Si es un POST devuelvo la info del alumno nuevo
            elif request.method == 'POST':
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    resul = Alumno.objects.create_user(**serializer.validated_data)
                    if resul['status']:
                        return Response(utils.to_dict(resul))
                else:
                    raise
        except Exception as e:
            return Response(dict(status=False, message="Error en la llamada"))