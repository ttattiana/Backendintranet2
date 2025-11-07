from rest_framework import serializers
from .models import Herramienta, RegistroUso

# Serializer para manejar la creación y edición de Herramientas
class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramienta
        # Incluimos 'foto' y 'descripcion' para poder recibirlas en la API
        fields = ['id', 'nombre', 'serial', 'equipo_id', 'foto', 'descripcion', 'fecha_registro']
        read_only_fields = ['fecha_registro'] # Estos se establecen automáticamente

# Serializer para manejar el registro de uso al escanear el QR
class RegistroUsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroUso
        # Incluimos todos los campos para el registro de escaneo (incluyendo la foto de evidencia)
        fields = '__all__'
        read_only_fields = ['fecha_uso']