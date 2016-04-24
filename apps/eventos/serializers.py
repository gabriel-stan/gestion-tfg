from rest_framework import serializers
from eventos.models import Evento


class EventoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Evento
        fields = ('id', 'contenido', 'tipo', 'autor')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        return Evento.objects.create_user(**validated_data)
