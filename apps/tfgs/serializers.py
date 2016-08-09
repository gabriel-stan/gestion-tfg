import utils
from django.db import models
from rest_framework import serializers
from tfgs.models import Tfg, Tfg_Asig, Titulacion
from authentication.models import Profesor
from authentication.serializers import ProfesorSerializer
from eventos.models import Tipo_Evento, SubTipo_Evento


class TitulacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titulacion
        fields = ('id', 'codigo', 'nombre',)

    def update(self, titulacion, validated_data):
        try:
            # comprobando codigo
            if 'codigo' in validated_data.keys():
                new_codigo = validated_data.get('codigo')
                try:
                    res = Titulacion.objects.filter(codigo=new_codigo)
                except:
                    raise NameError('La Titulacion no existe')
                if res.count() != 0:
                    raise NameError("El departamento ya existe")
                elif not isinstance(new_codigo, basestring):
                    raise NameError("El codigo de la titulacion no tiene formato correcto")
                else:
                    titulacion.codigo = new_codigo

            # comprobando nombre
            if 'nombre' in validated_data.keys():
                new_nombre = validated_data.get('nombre')
                if not isinstance(new_nombre, basestring):
                    raise NameError("El nombre de la titulacion no tiene formato correcto")
                else:
                    titulacion.nombre = new_nombre

            titulacion.save()

            return dict(status=True, data=titulacion)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")

    def delete(self, titulacion):
        titulacion.delete()
        return dict(status=True)


class TfgSerializer(serializers.ModelSerializer):
    # tutor = ProfesorSerializer()
    # cotutor = ProfesorSerializer()
    # titulacion = TitulacionSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Tfg
        fields = ('id', 'tipo', 'titulo', 'updated_at', 'n_alumnos', 'descripcion', 'conocimientos_previos',
                  'hard_soft', 'tutor', 'cotutor', 'created_at', 'updated_at', 'titulacion', 'publicado', 'validado',
                  'asignado')
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        return Tfg.objects.create(**validated_data)

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
                try:
                    tutor = Profesor.objects.get(email=validated_data.get('tutor'))
                except:
                    raise NameError('El tutor no existe')
                if not isinstance(tutor, Profesor) or tutor.groups.filter(name='Profesores').exists():
                    raise NameError("Tutor incorrecto")
                else:
                    tfg.tutor = tutor

            # comprobando cotutor
            if 'cotutor' in validated_data.keys():
                try:
                    cotutor = Profesor.objects.get(email=validated_data.get('cotutor'))
                except:
                    raise NameError("El Cotutor no existe")
                if not isinstance(cotutor, Profesor) or not cotutor.groups.filter(name='Profesores').exists():
                    raise NameError("Cotutor incorrecto")
                else:
                    tfg.cotutor = cotutor

            # comprobando titulacion
            if 'titulacion' in validated_data.keys():
                try:
                    titulacion = Titulacion.objects.get(codigo=validated_data.get('titulacion'))
                except:
                    raise NameError('La Titulacion no existe')
                if not isinstance(titulacion, Titulacion):
                    raise NameError("Titulacion incorrecta")
                else:
                    tfg.titulacion = titulacion

            # comprobando publicado
            if 'publicado' in validated_data.keys():
                if validated_data.get('publicado') == '' or not utils.is_bool(validated_data.get('publicado')):
                    raise NameError("Valor Publicado invalido")
                else:
                    tfg.publicado = bool(validated_data.get('publicado'))

            # comprobando validado
            if 'validado' in validated_data.keys():
                if validated_data.get('validado') == '' or not utils.is_bool(validated_data.get('validado')):
                    raise NameError("Valor Validado invalido")
                else:
                    tfg.validado = bool(validated_data.get('validado'))

            # comprobando asignado
            if 'asignado' in validated_data.keys():
                if validated_data.get('asignado') == '' or not utils.is_bool(validated_data.get('asignado')):
                    raise NameError("Valor Publicado invalido")
                else:
                    try:
                        tfg_asig = Tfg_Asig.objects.get(tfg=tfg)
                    except:
                        raise NameError('El Tfg asignado no existe')
                    if validated_data.get('asignado'):
                        tfg.asignado = bool(validated_data.get('asignado'))
                    else:
                        try:
                            resul = self.serializer_class(tfg_asig).delete
                            tfg.asignado = bool(validated_data.get('asignado'))
                        except:
                            raise NameError('Error al eliminar la asignacion del tfg')

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
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Tfg_Asig
        fields = ('id', 'tfg', 'alumno_1', 'alumno_2', 'alumno_3', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)

    def create_tfg_asig(self, validated_data):
        return Tfg_Asig.objects.create_tfg_asig(**validated_data)

    def update(self, tfg_asig, validated_data):
        try:
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
                    tfg_asig.convocatoria = res_tipo

            tfg_asig.save()

            return dict(status=True, data=Tfg_Asig.objects.get(tfg=tfg_asig.tfg))
        except NameError as e:
            return dict(status=False, message=e.message)

    def delete(self, tfg_asig):
        tfg_asig.delete()
        return dict(status=True)