import re
import utils
from django.db import models
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.serializers import ProfesorSerializer
from authentication.models import Profesor
from comisiones_evaluacion.models import Comision_Evaluacion, Tribunales
from eventos.models import Tipo_Evento, SubTipo_Evento
from tfgs.models import Tfg_Asig, Tfg
from tfgs.serializers import Tfg_AsigSerializer
from datetime import datetime
import hashlib as hl
import random
from django.contrib.auth.models import Group


class Comision_EvaluacionSerializer(serializers.ModelSerializer):
    presidente = ProfesorSerializer()
    vocal_1 = ProfesorSerializer()
    vocal_2 = ProfesorSerializer()
    suplente_1 = ProfesorSerializer()
    suplente_2 = ProfesorSerializer()

    class Meta:
        model = Comision_Evaluacion
        fields = ('id', 'presidente', 'vocal_1', 'vocal_2', 'suplente_1',
                  'suplente_2')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        return Comision_Evaluacion.objects.create_user(**validated_data)

    def update(self, user, comision, validated_data):
        try:
            # comprobando presidente
            if 'presidente' in validated_data.keys():
                try:
                    presidente = Profesor.objects.get(email=validated_data.get('presidente'))
                    posicion, id_comision = utils.check_miembro(comision, presidente)
                    comision_intercambiar = Comision_Evaluacion.objects.get(id=id_comision)
                    if not posicion:
                        comision.presidente = presidente
                    elif utils.check_miembro_repetido(comision_intercambiar,
                                                      comision.presidente.email) and utils.check_miembro_repetido(
                            comision, presidente):
                        utils.intercambiar_miembros(comision, comision_intercambiar, 'presidente', posicion)
                    comision_intercambiar.save()
                except Profesor.DoesNotExist:
                    raise NameError('El presidente no existe')

            # comprobando primer titular
            if 'titular_1' in validated_data.keys():
                try:
                    titular_1 = Profesor.objects.get(email=validated_data.get('titular_1'))
                    if not utils.check_miembro(comision, titular_1):
                        raise NameError('El cambio no esta permitido')
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
                    if not utils.check_miembro(comision, titular_2):
                        raise NameError('El cambio no esta permitido')
                except:
                    raise NameError('El segundo vocal')
                if not isinstance(titular_2, Profesor) or titular_2.groups.filter(name='Profesores').exists():
                    raise NameError("Segundo titular incorrecto")
                else:
                    comision.titular_2 = titular_2

            # comprobando primer suplente
            if 'suplente_1' in validated_data.keys():
                try:
                    suplente_1 = Profesor.objects.get(email=validated_data.get('sup_presidente'))
                    if not utils.check_miembro(comision, suplente_1):
                        raise NameError('El cambio no esta permitido')
                except:
                    raise NameError('El suplente del presidente no existe')
                if not isinstance(suplente_1, Profesor) or suplente_1.groups.filter(name='Profesores').exists():
                    raise NameError("Suplente del presidente incorrecto")
                else:
                    comision.suplente_1 = suplente_1

            # comprobando suplente del primer titular
            if 'suplente_2' in validated_data.keys():
                try:
                    suplente_2 = Profesor.objects.get(email=validated_data.get('suplente_2'))
                    if not utils.check_miembro(comision, suplente_2):
                        raise NameError('El cambio no esta permitido')
                except:
                    raise ('El suplente del primer vocal no existe')
                if not isinstance(suplente_2, Profesor) or suplente_2.groups.filter(name='Profesores').exists():
                    raise NameError("Suplente del primer titular incorrecto")
                else:
                    comision.suplente_2 = suplente_2

            # comprobando convocatoria
            if 'convocatoria' in validated_data.keys():
                try:
                    res_tipo = Tipo_Evento.objects.get(codigo=validated_data.get('convocatoria'))
                except:
                    raise NameError("La convocatoria no existe")
                try:
                    res_subtipo = SubTipo_Evento.objects.get(codigo=validated_data.get('tipo'))
                except:
                    raise NameError("El Tipo no existe")
                if not utils.check_convocatoria(res_tipo, res_subtipo):
                    raise NameError("Fuera de plazo")
                else:
                    comision.convocatoria = res_tipo

            comision.save()

            return dict(status=True, data=Comision_Evaluacion.objects.get(presidente=comision.presidente).to_dict(user))
        except NameError as e:
            return dict(status=False, message=e.message)

    def delete(self, comision):
        try:
            Comision_Evaluacion.objects.get(presidente=comision.presidente).delete()
            return dict(status=True)
        except Comision_Evaluacion.DoesNotExist:
            return dict(status=False, message="La comision no existe")


class TribunalesSerializer(serializers.ModelSerializer):
    tfg = Tfg_AsigSerializer()
    comision = Comision_EvaluacionSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Tribunales
        fields = ('id', 'tfg', 'comision', 'observaciones', 'fecha', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        return Tribunales.objects.create(**validated_data)

    def update(self, user, tribunal, validated_data):
        try:

            # comprobando comision
            if 'presidente' in validated_data.keys():
                try:
                    new_comision = Comision_Evaluacion.objects.get(presidente=validated_data.get('presidente'))
                except:
                    raise NameError("La comision no existe")

                tribunal.comision = new_comision

            # comprobando tfg
            if 'tfg' in validated_data.keys():
                try:
                    new_tfg = Tfg_Asig.objects.get(tfg=validated_data.get('tfg'))
                except:
                    raise NameError("El tfg no existe")
                if utils.check_tfg_tribunal(new_tfg):
                    tribunal.tfg = new_tfg
                else:
                    raise NameError("El TFG ya esta asignado a un tribunal")

            # comprobando observaciones
            if 'observaciones' in validated_data.keys():
                new_observaciones = validated_data.get('observaciones')
                if not isinstance(new_observaciones, basestring):
                    raise NameError("Las observaciones no tienen formato correcto")
                else:
                    tribunal.observaciones = new_observaciones

            # comprobando hasta
            if 'fecha' in validated_data.keys():
                try:
                    new_fecha = datetime.strptime(validated_data.get('fecha')[:19], '%Y-%m-%dT%H:%M:%S')
                except:
                    raise NameError("Error en formato fecha")
                tribunal.fecha = new_fecha

            tribunal.save()
            return dict(status=True, data=Tribunales.objects.get(tfg=tribunal.tfg, alumno=tribunal.alumno).to_dict(user))
        except NameError as e:
            return dict(status=False, message=e.message)

    def delete(self, tribunal):
        try:
            Tribunales.objects.get(alumno=tribunal.alumno).delete()
            return dict(status=True)
        except Tribunales.DoesNotExist:
            return dict(status=False, message="El tribunal no existe")