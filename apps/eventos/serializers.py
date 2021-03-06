from django.db import models
from rest_framework import serializers
from eventos.models import Evento, Tipo_Evento, SubTipo_Evento, Periodo, Convocatoria
from authentication.serializers import UsuarioSerializer
from authentication.models import Usuario
from datetime import datetime
import json


# class EventoSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
class EventoSerializer(serializers.ModelSerializer):
    #autor = UsuarioSerializer()
    convocatoria = models.ForeignKey(Tipo_Evento)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Evento
        fields = ('id', 'contenido', 'convocatoria', 'autor', 'titulo', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create_evento(self, validated_data):
        return Evento.objects.create_evento(**validated_data)

    def update(self, evento, validated_data):
        try:
            # comprobando contenido
            if 'contenido' in validated_data.keys():
                new_contenido = validated_data.get('contenido')
                if not isinstance(new_contenido, basestring):
                    raise NameError("Error en el contenido")
                else:
                    evento.contenido = new_contenido

            # comprobando convocatoria
            # if 'convocatoria' in validated_data.keys():
            #     new_convocatoria = validated_data.get('convocatoria')
            #     try:
            #         convocatoria = Convocatoria.objects.get(codigo=new_convocatoria)
            #     except Tipo_Evento.DoesNotExist:
            #         raise NameError("Convocatoria incorrecto")
            #     evento.convocatoria = convocatoria

            # comprobando tipo
            if 'tipo' in validated_data.keys():
                new_tipo = validated_data.get('tipo')
                try:
                    tipo = SubTipo_Evento.objects.get(codigo=new_tipo)
                except SubTipo_Evento.DoesNotExist:
                    raise NameError("Tipo Evento incorrecto")
                evento.tipo = tipo

            # comprobando autor
            # if 'autor' in validated_data.keys():
            #     new_autor = validated_data.get('autor')
            #     autor = Usuario.objects.get(email=new_autor)
            #     if not isinstance(autor, Usuario):
            #         raise NameError("Autor incorrecto")
            #     else:
            #         evento.autor = autor

            # comprobando titulo
            if 'titulo' in validated_data.keys():
                new_titulo = validated_data.get('titulo')
                if not isinstance(new_titulo, basestring):
                    raise NameError("El titulo del evento no tiene formato correcto")
                else:
                    evento.titulo = new_titulo

            # comprobando desde
            if 'desde' in validated_data.keys():
                try:
                    new_desde = datetime.strptime(validated_data.get('desde')[:19], '%Y-%m-%dT%H:%M:%S')
                except:
                    raise NameError("Error en formato fecha desde")

            # comprobando hasta
            if 'hasta' in validated_data.keys():
                try:
                    new_hasta = datetime.strptime(validated_data.get('hasta')[:19], '%Y-%m-%dT%H:%M:%S')
                except:
                    raise NameError("Error en formato fecha hasta")

            # Actualizo el periodo
            if 'hasta' in validated_data.keys() or 'desde' in validated_data.keys():
                periodo = Periodo.objects.get(evento=evento)
                if 'hasta' in validated_data.keys():
                    periodo.end = new_hasta
                if 'desde' in validated_data.keys():
                    periodo.start = new_desde
                periodo.save()
            evento.save()
            return dict(status=True, data=EventoSerializer(Evento.objects.get(contenido=evento.contenido)).data)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")

    def delete(self, evento):
        evento.delete()
        return dict(status=True)


class Tipo_EventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tipo_Evento
        fields = ('id', 'codigo', 'nombre',)

    def create(self, validated_data):
        return Tipo_Evento.objects.create_tipo_evento(**validated_data)

    def update(self, tipo_evento, validated_data):
        try:
            # comprobando codigo
            if 'codigo' in validated_data.keys():
                new_codigo = validated_data.get('codigo')
                res = Tipo_Evento.objects.filter(codigo=new_codigo)
                if res.count() != 0:
                    raise NameError("El tipo de evento ya existe")
                elif not isinstance(new_codigo, basestring):
                    raise NameError("El codigo del tipo de evento no tiene formato correcto")
                else:
                    tipo_evento.codigo = new_codigo

            # comprobando nombre
            if 'nombre' in validated_data.keys():
                new_nombre = validated_data.get('nombre')
                if not isinstance(new_nombre, basestring):
                    raise NameError("El nombre del tipo de evento no tiene formato correcto")
                else:
                    tipo_evento.nombre = new_nombre

            tipo_evento.save()

            return dict(status=True, data=tipo_evento)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")

    def delete(self, tipo_evento):
        tipo_evento.delete()
        return dict(status=True)


class SubTipo_EventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTipo_Evento
        fields = ('id', 'codigo', 'nombre',)

    def update(self, subtipo, validated_data):
        try:
            # comprobando codigo
            if 'codigo' in validated_data.keys():
                new_codigo = validated_data.get('codigo')
                res = SubTipo_Evento.objects.filter(codigo=new_codigo)
                if res.count() != 0:
                    raise NameError("El departamento ya existe")
                elif not isinstance(new_codigo, basestring):
                    raise NameError("El codigo del subtipo no tiene formato correcto")
                else:
                    subtipo.codigo = new_codigo

            # comprobando nombre
            if 'nombre' in validated_data.keys():
                new_nombre = validated_data.get('nombre')
                if not isinstance(new_nombre, basestring):
                    raise NameError("El nombre del subtipo no tiene formato correcto")
                else:
                    subtipo.nombre = new_nombre

            subtipo.save()

            return dict(status=True, data=subtipo)

        except NameError as e:
            return dict(status=False, message=e.message)
        except:
            return dict(status=False, message="Error en los parametros")

    def delete(self, subtipo):
        subtipo.delete()
        return dict(status=True)
