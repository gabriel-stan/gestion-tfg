__author__ = 'tonima'
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.response import Response
from controller.servicios import tfg_services, utils


@api_view(['POST'])
def login(request):
    try:
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return Response(dict(status=True, message="OK"))
            else:
                return Response(dict(status=False, message="La cuenta no esta activa"))
        else:
            return Response(dict(status=False, message="Login Invalido"))
    except Exception as e:
        return Response(dict(status=False, message="Error en la llamada"))