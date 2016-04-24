__author__ = 'tonima'
from models import Alumno, Profesor, Tfg
from rest_framework import serializers


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id', 'username', 'first_name', 'last_name')


class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ('id', 'username', 'first_name', 'last_name', 'departamento')


class TFGSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tfg
        fields = ('id', 'tipo', 'titulo', 'n_alumnos', 'descripcion', 'conocimientos_previos', 'hard_soft',
                  'tutor', 'cotutor')
