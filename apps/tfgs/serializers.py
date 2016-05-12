import re
import utils
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from tfgs.models import Tfg, Tfg_Asig
from authentication.models import Profesor, Alumno


class TfgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tfg
        fields = ('id', 'tipo', 'titulo', 'updated_at', 'n_alumnos', 'descripcion', 'conocimientos_previos',
                  'hard_soft', 'tutor', 'cotutor', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        return Tfg.objects.create_tfg(**validated_data)

    def update(self, tfg, validated_data):
        try:
            # comprobando titulo
            if 'titulo' in validated_data.keys():
                if validated_data.get('titulo') == '' or not utils.is_string(validated_data.get('titulo')):
                    raise NameError("Titulo incorrecto")
                else:
                    tfg.titulo = validated_data.get('titulo')
            # comprobando tipo
            if 'tipo' in validated_data.keys():
                if validated_data.get('tipo') == '' or not utils.is_string(validated_data.get('tipo')):
                    raise NameError("Tipo incorrecto")
                else:
                    tfg.tipo = validated_data.get('tipo')

            # comprobando n_alumnos
            if 'n_alumnos' in validated_data.keys():
                if (validated_data.get('n_alumnos') <= 0) or (validated_data.get('n_alumnos') > 3) or \
                        not (isinstance(validated_data.get('n_alumnos'), int)):
                    raise NameError("Numero de alumnos incorrecto")
                else:
                    tfg.n_alumnos = validated_data.get('n_alumnos')

            # comprobando descripcion
            if 'descripcion' in validated_data.keys():
                if validated_data.get('descripcion') == '' or not utils.is_string(validated_data.get('descripcion')):
                    raise NameError("Descripcion incorrecta")
                else:
                    tfg.descripcion = validated_data.get('descripcion')

            # comprobando conocimientos_previos
            if 'conocimientos_previos' in validated_data.keys():
                if validated_data.get('conocimientos_previos') == '' or \
                        not utils.is_string(validated_data.get('conocimientos_previos')):
                    raise NameError("Conocimientos Previos incorrectos")
                else:
                    tfg.conocimientos_previos = validated_data.get('conocimientos_previos')

            # comprobando hard_soft
            if 'hard_soft' in validated_data.keys():
                if validated_data.get('hard_soft') == '' or not utils.is_string(validated_data.get('hard_soft')):
                    raise NameError("Hard/Soft incorrectos")
                else:
                    tfg.hard_soft = validated_data.get('hard_soft')

            # comprobando tutor
            if 'tutor' in validated_data.keys():
                tutor = Profesor.objects.get(email=validated_data.get('tutor'))
                if not isinstance(tutor, Profesor) or tutor.groups.filter(name='Profesores').exists():
                    raise NameError("Tutor incorrecto")
                else:
                    tfg.tutor = tutor

            # comprobando cotutor
            if 'cotutor' in validated_data.keys():
                cotutor = Profesor.objects.get(email=validated_data.get('cotutor'))
                if not isinstance(cotutor, Profesor) or not cotutor.groups.filter(name='Profesores').exists():
                    raise NameError("CoTutor incorrecto")
                else:
                    tfg.tutor = cotutor

            tfg.save()

            return dict(status=True, data=Tfg.objects.get(titulo=tfg.titulo))
        except NameError as e:
            return dict(status=False, message=e.message)

    def delete(self, tfg):
        try:
            Tfg.objects.get(titulo=tfg.titulo).delete()
            return dict(status=True)
        except Tfg.DoesNotExist:
            return dict(status=False, message="El Tfg no existe")


class Tfg_AsigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tfg_Asig
        fields = ('id', 'tfg', 'alumno_1', 'alumno_2', 'alumno_3', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)

    def create_tfg_asig(self, validated_data):
        return Tfg_Asig.objects.create_tfg_asig(**validated_data)
