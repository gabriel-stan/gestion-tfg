from rest_framework import serializers
from eventos.models import Evento


class EventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evento
        fields = ('id', 'contenido', 'tipo', 'autor')
        read_only_fields = ('created_at', 'updated_at')

    def create_evento(self, validated_data):
        return Evento.objects.create_evento(**validated_data)
