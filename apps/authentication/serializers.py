import re
import utils
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Alumno, Profesor


class AlumnoSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True, required=False)
    #confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Alumno
        fields = ('id', 'email', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        return Alumno.objects.create_user(**validated_data)

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
                    raise NameError("El alumno indicado no existe")

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
            return dict(status=False, message="El email no es correcto")

    def delete_alumno(self, alumno):
        try:
            Alumno.objects.get(email=alumno.email).delete()
            return dict(status=True)
        except Alumno.DoesNotExist:
            return dict(status=False, message="El alumno no existe")


class ProfesorSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True, required=False)
    #confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profesor
        fields = ('id', 'email', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password', 'departamento')
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        return Profesor.objects.create_user(**validated_data)

    def update(self, profesor, validated_data):
        try:
            # comprobando username
            if 'email' in validated_data.keys():
                new_email = validated_data.get('email')
                res = Profesor.objects.filter(email=new_email)
                if res.count() == 0:
                    if not (re.match(r'^[a-z][_a-z0-9]+(@ugr\.es)$', new_email)):
                        raise NameError("El email no es correcto")
                    else:
                        profesor.username = new_email
                else:
                    raise NameError("No existe el profesor")

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
                if new_departamento == '' or not utils.is_string(new_departamento):
                    raise NameError("Error en el departamento")
                else:
                    profesor.departamento = new_departamento

            profesor.save()

            return dict(status=True, data=profesor)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="El email no es correcto")

    def delete(self, profesor):

        try:
            Profesor.objects.get(email=profesor.email).delete()
            return dict(status=True)
        except Profesor.DoesNotExist:
            return dict(status=False, message="El profesor no existe")