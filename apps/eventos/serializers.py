from django.db import models
from rest_framework import serializers
from eventos.models import Evento, Tipo_Evento
from authentication.serializers import UsuarioSerializer
from authentication.models import Usuario


# class EventoSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
class EventoSerializer(serializers.ModelSerializer):
    autor = UsuarioSerializer()
    tipo = models.ForeignKey(Tipo_Evento)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Evento
        fields = ('id', 'contenido', 'tipo', 'autor', 'titulo', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create_evento(self, validated_data):
        return Evento.objects.create_evento(**validated_data)

    def update(self, evento, validated_data):
        try:
            # comprobando contenido
            if 'contenido' in validated_data.keys():
                new_contenido = validated_data.get('contenido')
                res = Evento.objects.filter(contenido=new_contenido)
                if res.count() != 0:
                    raise NameError("El evento ya existe")
                elif not isinstance(new_contenido, basestring):
                    raise NameError("El codigo del evento no tiene formato correcto")
                else:
                    evento.contenido = new_contenido

            # comprobando tipo
            if 'tipo' in validated_data.keys():
                new_tipo = validated_data.get('tipo')
                tipo = Tipo_Evento.objects.get(codigo=new_tipo)
                if not isinstance(tipo, Tipo_Evento):
                    raise NameError("Tipo_Evento incorrecto")
                else:
                    evento.tipo = tipo

            # comprobando tipo
            if 'autor' in validated_data.keys():
                new_autor = validated_data.get('autor')
                autor = Usuario.objects.get(email=new_autor)
                if not isinstance(autor, Usuario):
                    raise NameError("Autor incorrecto")
                else:
                    evento.autor = autor

            # comprobando tipo
            if 'titulo' in validated_data.keys():
                new_titulo = validated_data.get('titulo')
                if not isinstance(new_titulo, basestring):
                    raise NameError("El titulo del evento no tiene formato correcto")
                else:
                    evento.titulo = new_titulo

            evento.save()
            return dict(status=True, data=evento)

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
