__author__ = 'tonima'
from models import Alumno
from rest_framework import serializers


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ('id', 'username', 'first_name', 'last_name')
