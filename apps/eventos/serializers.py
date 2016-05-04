from rest_framework import serializers
from eventos.models import Evento
from authentication.serializers import UsuarioSerializer


# class EventoSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
class EventoSerializer(serializers.ModelSerializer):
    autor = UsuarioSerializer()
    #autor = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Evento
        fields = ('id', 'contenido', 'tipo', 'autor', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create_evento(self, validated_data):
        return Evento.objects.create_evento(**validated_data)
    #
    # def to_internal_value(self, data):
    #     return serializers.PrimaryKeyRelatedField.to_internal_value(self, data)
    #
    # def to_representation(self, data):
    #     return serializers.ModelSerializer.to_representation(self, data)
