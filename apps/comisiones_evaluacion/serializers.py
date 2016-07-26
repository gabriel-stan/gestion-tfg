import re
import utils
from django.db import models
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.serializers import ProfesorSerializer
from authentication.models import Profesor
from comisiones_evaluacion.models import Comision_Evaluacion
from django.contrib.auth.models import Group


class Comision_EvaluacionSerializer(serializers.ModelSerializer):
    presidente = ProfesorSerializer()
    titular_1 = ProfesorSerializer()
    titular_2 = ProfesorSerializer()
    sup_presidente = ProfesorSerializer()
    sup_titular_1 = ProfesorSerializer()
    sup_titular_2 = ProfesorSerializer()

    class Meta:
        model = Comision_Evaluacion
        fields = ('id', 'presidente', 'titular_1', 'titular_2', 'sup_presidente',
                  'sup_titular_1', 'sup_titular_2')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        return Comision_Evaluacion.objects.create_user(**validated_data)

    def update(self, comision, validated_data):
        try:
            # comprobando presidente
            if 'presidente' in validated_data.keys():
                try:
                    presidente = Profesor.objects.get(email=validated_data.get('presidente'))
                except:
                    raise NameError('El presidente no existe')
                if not isinstance(presidente, Profesor) or presidente.groups.filter(name='Profesores').exists():
                    raise NameError("Presidente incorrecto")
                else:
                    comision.presidente = presidente

            # comprobando primer titular
            if 'titular_1' in validated_data.keys():
                try:
                    titular_1 = Profesor.objects.get(email=validated_data.get('titular_1'))
                except:
                    raise NameError('El primer vocal no existe')
                if not isinstance(titular_1, Profesor) or titular_1.groups.filter(name='Profesores').exists():
                    raise NameError("Primer Titular incorrecto")
                else:
                    comision.titular_1 = titular_1

            # comprobando segundo titular
            if 'titular_2' in validated_data.keys():
                try:
                    titular_2 = Profesor.objects.get(email=validated_data.get('titular_2'))
                except:
                    raise NameError('El segundo vocal')
                if not isinstance(titular_2, Profesor) or titular_2.groups.filter(name='Profesores').exists():
                    raise NameError("Segundo titular incorrecto")
                else:
                    comision.titular_2 = titular_2

            # comprobando suplente del presidente
            if 'sup_presidente' in validated_data.keys():
                try:
                    sup_presidente = Profesor.objects.get(email=validated_data.get('sup_presidente'))
                except:
                    raise NameError('El suplente del presidente no existe')
                if not isinstance(sup_presidente, Profesor) or sup_presidente.groups.filter(name='Profesores').exists():
                    raise NameError("Suplente del presidente incorrecto")
                else:
                    comision.sup_presidente = sup_presidente

            # comprobando suplente del primer titular
            if 'sup_titular_1' in validated_data.keys():
                try:
                    sup_titular_1 = Profesor.objects.get(email=validated_data.get('sup_titular_1'))
                except:
                    raise ('El suplente del primer vocal no existe')
                if not isinstance(sup_titular_1, Profesor) or sup_titular_1.groups.filter(name='Profesores').exists():
                    raise NameError("Suplente del primer titular incorrecto")
                else:
                    comision.sup_titular_1 = sup_titular_1

            # comprobando suplente del titular 2
            if 'sup_titular_2' in validated_data.keys():
                sup_titular_2 = Profesor.objects.get(email=validated_data.get('sup_titular_2'))
                if not isinstance(sup_titular_2, Profesor) or sup_titular_2.groups.filter(name='Profesores').exists():
                    raise NameError("Suplente del segundo titular incorrecto")
                else:
                    comision.sup_titular_2 = sup_titular_2

            comision.save()

            return dict(status=True, data=Comision_Evaluacion.objects.get(presidente=comision.presidente))
        except NameError as e:
            return dict(status=False, message=e.message)

    def delete(self, comision):
        try:
            Comision_Evaluacion.objects.get(presidente=comision.presidente).delete()
            return dict(status=True)
        except Comision_Evaluacion.DoesNotExist:
            return dict(status=False, message="La comision no existe")
