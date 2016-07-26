import re
import utils
from django.db import models
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Alumno, Profesor, Usuario, Departamento, Grupos
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UsuarioSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'dni', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password', 'is_admin', 'groups')
        read_only_fields = ('created_at', 'updated_at', 'is_admin')

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)

    def update(self, usuario, validated_data):
        try:
            # comprobando email
            if 'email' in validated_data.keys():
                new_email = validated_data.get('email')
                res = Usuario.objects.filter(email=new_email)
                if res.count() == 0:
                    if not utils.is_string(new_email) or not \
                            re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$', new_email):
                        raise NameError("El email no es correcto")
                    else:
                        usuario.email = new_email
                else:
                    raise NameError("El usuario indicado ya existe")

            # comprobando dni
            if 'dni' in validated_data.keys():
                new_dni = validated_data.get('dni')
                res = Usuario.objects.filter(dni=new_dni)
                if res.count() == 0:
                    if not utils.is_string(new_dni) or not \
                            re.match(r'(\d{8})([-]?)([A-Z]{1})', new_dni):
                        raise NameError("El dni no es correcto")
                    else:
                        usuario.email = new_dni
                else:
                    raise NameError("El usuario indicado ya existe")

            # comprobando nombre
            if 'first_name' in validated_data.keys():
                new_first_name = validated_data.get('first_name')
                if new_first_name == '' or not utils.is_string(new_first_name):
                    raise NameError("Nombre incorrecto")
                else:
                    usuario.first_name = new_first_name

            # comprobando apellidos
            if 'last_name' in validated_data.keys():
                new_last_name = validated_data.get('last_name')
                if new_last_name == '' or not utils.is_string(new_last_name):
                    raise NameError("Nombre incorrecto")
                else:
                    usuario.new_last_name = new_last_name

            # if 'password' in validated_data.keys() and 'confirm_password' in validated_data.keys():
            #     password = validated_data.get('password')
            #     confirm_password = validated_data.get('confirm_password')
            #     if password and confirm_password and password == confirm_password:
            #         alumno.set_password(password)

            usuario.save()

            return dict(status=True, data=usuario)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")


class DepartamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departamento
        fields = ('id', 'codigo', 'nombre',)

    def update(self, departamento, validated_data):
        try:
            # comprobando codigo
            if 'codigo' in validated_data.keys():
                new_codigo = validated_data.get('codigo')
                res = Departamento.objects.filter(codigo=new_codigo)
                if res.count() != 0:
                    raise NameError("El departamento ya existe")
                elif not isinstance(new_codigo, basestring):
                    raise NameError("El codigo del departamento no tiene formato correcto")
                else:
                    departamento.codigo = new_codigo

            # comprobando nombre
            if 'nombre' in validated_data.keys():
                new_nombre = validated_data.get('nombre')
                if not isinstance(new_nombre, basestring):
                    raise NameError("El nombre del departamento no tiene formato correcto")
                else:
                    departamento.nombre = new_nombre

            departamento.save()

            return dict(status=True, data=departamento)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")

    def delete(self, departamento):
        departamento.delete()
        return dict(status=True)


class AlumnoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Alumno
        fields = ('id', 'email', 'dni', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        if validated_data.get('email') or validated_data.get('dni'):
            return Alumno.objects.create_user(**validated_data)
        return dict(status=False, message='Error en parametros')

    def update(self, alumno, validated_data):
        try:
            # comprobando email
            if 'email' in validated_data.keys():
                new_email = validated_data.get('email')
                res = Alumno.objects.filter(email=new_email)
                if res.count() == 0:
                    if not utils.is_string(new_email) or not \
                            re.match(r'^[a-z][_a-z0-9]+(@correo\.ugr\.es)$', new_email):
                        raise NameError("El email no es correcto")
                    else:
                        alumno.email = new_email
                else:
                    raise NameError("El alumno indicado ya existe")

            # comprobando dni
            if 'dni' in validated_data.keys():
                new_dni = validated_data.get('dni')
                res = Alumno.objects.filter(dni=new_dni)
                if res.count() == 0:
                    if not utils.is_string(new_dni) or not \
                            re.match(r'(\d{8})([-]?)([A-Z]{1})', new_dni):
                        raise NameError("El dni no es correcto")
                    else:
                        alumno.email = new_dni
                else:
                    raise NameError("El alumno indicado ya existe")

            # comprobando nombre
            if 'first_name' in validated_data.keys():
                new_first_name = validated_data.get('first_name')
                if new_first_name == '' or not utils.is_string(new_first_name):
                    raise NameError("Nombre incorrecto")
                else:
                    alumno.first_name = new_first_name

            # comprobando apellidos
            if 'last_name' in validated_data.keys():
                new_last_name = validated_data.get('last_name')
                if new_last_name == '' or not utils.is_string(new_last_name):
                    raise NameError("Nombre incorrecto")
                else:
                    alumno.new_last_name = new_last_name

            # if 'password' in validated_data.keys() and 'confirm_password' in validated_data.keys():
            #     password = validated_data.get('password')
            #     confirm_password = validated_data.get('confirm_password')
            #     if password and confirm_password and password == confirm_password:
            #         alumno.set_password(password)

            alumno.save()

            return dict(status=True, data=alumno)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")

    def delete(self, alumno):
        alumno.delete()
        return dict(status=True)


class ProfesorSerializer(serializers.ModelSerializer):
    departamento = models.ForeignKey(Departamento)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    jefe_departamento = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Profesor
        fields = ('id', 'email', 'dni', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password', 'departamento', 'jefe_departamento')
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        return Profesor.objects.create_user(**validated_data)

    def update(self, profesor, validated_data):
        try:
            # comprobando email
            if 'email' in validated_data.keys():
                new_email = validated_data.get('email')
                res = Profesor.objects.filter(email=new_email)
                if res.count() == 0:
                    if not (re.match(r'^[a-z][_a-z0-9]+(@ugr\.es)$', new_email)):
                        raise NameError("El email no es correcto")
                    else:
                        profesor.email = new_email
                else:
                    raise NameError("El profesor indicado ya existe")

            # comprobando dni
            if 'dni' in validated_data.keys():
                new_dni = validated_data.get('dni')
                res = Profesor.objects.filter(dni=new_dni)
                if res.count() == 0:
                    if not utils.is_string(new_dni) or not \
                            re.match(r'(\d{8})([-]?)([A-Z]{1})', new_dni):
                        raise NameError("El dni no es correcto")
                    else:
                        profesor.email = new_dni
                else:
                    raise NameError("El profesor indicado ya existe")

            # comprobando nombre
            if 'first_name' in validated_data.keys():
                new_first_name = validated_data.get('first_name')
                if new_first_name == '' or not utils.is_string(new_first_name):
                    raise NameError("Error en el nombre del profesor")
                else:
                    profesor.first_name = new_first_name

            # comprobando apellidos
            if 'last_name' in validated_data.keys():
                new_last_name = validated_data.get('last_name')
                if new_last_name == '' or not utils.is_string(new_last_name):
                    raise NameError("Error en los apellidos del profesor")
                else:
                    profesor.last_name = new_last_name

            # comprobando departamento
            if 'departamento' in validated_data.keys():
                new_departamento = validated_data.get('departamento')
                try:
                    departamento = Departamento.objects.get(codigo=new_departamento)
                except:
                    raise NameError('El departamento no existe')
                if not isinstance(departamento, Departamento):
                    raise NameError("Departamento incorrecto")
                else:
                    profesor.departamento = departamento

            # comprobando si es Jefe de departamento
            if 'jefe_departamento' in validated_data.keys():
                try:
                    grupo_jefe_departamento = Grupos.objects.get(name='Jefe de Departamento')
                except:
                    raise NameError('El grupo Jefe de departamento no existe')
                if validated_data.get('jefe_departamento') == True:
                    grupo_jefe_departamento.user_set.add(profesor)
                else:
                    grupo_jefe_departamento.user_set.remove(profesor)

            profesor.save()

            return dict(status=True, data=profesor)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")

    def delete(self, profesor):
        profesor.delete()
        return dict(status=True)