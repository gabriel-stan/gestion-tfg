__author__ = 'tonima'
from models import Alumno, Profesor
from rest_framework import serializers


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id', 'username', 'first_name', 'last_name')

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ('id', 'username', 'first_name', 'last_name', 'departamento')
