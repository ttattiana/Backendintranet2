from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
import uuid

# ====================================================================
# MODELOS
# ====================================================================

# Modelo de Perfil de Usuario extendido
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('SUPERVISOR', 'Supervisor'),
        ('TECNICO', 'tecnico'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='OPERADOR')
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'

# Modelo de Herramienta (MODIFICADO para foto y descripción)
class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    serial = models.CharField(max_length=100, unique=True)
    equipo_id = models.CharField(max_length=50)
    # 🛑 NUEVO: Campo para la foto al registrar la herramienta
    foto = models.ImageField(upload_to='herramientas_fotos/', null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# MODELO AGREGADO: LoginChallenge
class LoginChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_valid(self):
        return self.expires_at > timezone.now()

    def __str__(self):
        return f"Challenge para {self.user.username}"


# 🛑 NUEVO MODELO: Registro de uso (para capturar la info del escaneo)
class RegistroUso(models.Model):
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    # Asumimos que el usuario es quien escanea el QR
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Información del formulario que diligencias en el celular
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    ESTADOS = [
        ('BUENO', 'Bueno'), 
        ('MALO', 'Malo'),
        ('REPARACION', 'En Reparación'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS, default='BUENO')
    observaciones = models.TextField(blank=True, null=True)
    
    # Campo para la foto de evidencia tomada al escanear
    foto_evidencia = models.ImageField(upload_to='uso_fotos/', null=True, blank=True)
    
    fecha_uso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Uso de {self.herramienta.nombre} el {self.fecha_uso.strftime('%Y-%m-%d')}"


# ====================================================================
# SEÑALES (Signals) - Se mantienen igual
# ====================================================================

# Crea un objeto Profile automáticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        Profile.objects.create(user=instance)

# Asegura que el Profile se guarde
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile') and not kwargs.get('raw', False):
        instance.profile.save()
    