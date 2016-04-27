from rest_framework import serializers
from eventos.models import Evento
from authentication.serializers import UsuarioSerializer


class EventoSerializer(serializers.ModelSerializer):
    autor = UsuarioSerializer()

    class Meta:
        model = Evento
        fields = ('id', 'contenido', 'tipo', 'autor')
        read_only_fields = ('created_at', 'updated_at')

    def create_evento(self, validated_data):
        return Evento.objects.create_evento(**validated_data)
