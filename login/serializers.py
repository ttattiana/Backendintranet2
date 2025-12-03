from rest_framework import serializers
from .models import Herramienta, RegistroUso
from django.contrib.auth.models import User # Importamos el modelo de Usuario de Django

# --- 1. Serializer para Herramienta ---
class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramienta
        fields = ['id', 'nombre', 'serial', 'equipo_id', 'foto', 'descripcion', 'fecha_registro']
        read_only_fields = ['fecha_registro']

# --- 2. Serializer para información básica del Usuario ---
class UserSerializer(serializers.ModelSerializer):
    """Serializa la información básica del usuario (nombre y apellido)."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
# --- 3. Serializer principal para Registro de Uso (Corregido) ---
class RegistroUsoSerializer(serializers.ModelSerializer):
    """
    Serializa el registro de uso, incluyendo la información enriquecida 
    del usuario y el serial de la herramienta.
    """
    # Campos enriquecidos para la respuesta
    usuario_info = UserSerializer(source='usuario', read_only=True)
    serial_herramienta = serializers.CharField(source='herramienta.serial', read_only=True)

    class HerramientaSerializer(serializers.ModelSerializer):
     class Meta:
        model = Herramienta
        # ✅ AJUSTE: Volvemos a usar 'fecha_registro'
        fields = ['id', 'nombre', 'serial', 'equipo_id', 'foto', 'descripcion', 'fecha_registro']
        # ✅ AJUSTE: Volvemos a usar 'fecha_registro'
        read_only_fields = ['fecha_registro']