from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Herramienta, Profile, RegistroUso, create_user_profile, save_user_profile 


# ====================================================================
# 1. Inline para inyectar el Profile
# ====================================================================

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user' 
    fieldsets = (
        (None, {
            'fields': ('rol', 'phone',), 
        }),
    )
    def has_add_permission(self, request, obj=None):
        return obj is not None


# ====================================================================
# 2. Reemplazo del administrador de usuarios por defecto
# ====================================================================

class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')

    def get_rol(self, obj):
        try:
            return obj.profile.rol
        except Profile.DoesNotExist:
            return 'N/A'
    get_rol.short_description = 'Rol'

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return [] 
        return super().get_inline_instances(request, obj)

    def save_model(self, request, obj, form, change):
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)
        
        try:
            super().save_model(request, obj, form, change)
            
            if not change:
                Profile.objects.create(user=obj) 
        finally:
            post_save.connect(create_user_profile, sender=User)
            post_save.connect(save_user_profile, sender=User)


# ====================================================================
# 3. Registro de Modelos
# ====================================================================

# Anular el registro del modelo User original y registrar el nuevo CustomUserAdmin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)


# Registrar el modelo Herramienta
@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'serial', 'equipo_id', 'fecha_registro')
    search_fields = ('nombre', 'serial', 'equipo_id')


# 🛑 REGISTRO DEL MODELO DE USO (Corregido con 'usuario' y 'fecha_uso') 🛑
@admin.register(RegistroUso)
class RegistroUsoAdmin(admin.ModelAdmin):
    # Usa los nombres REALES de tu models.py
    list_display = ('herramienta', 'usuario', 'estado', 'fecha_uso')
    
    # Usa el nombre REAL del campo de fecha
    list_filter = ('estado', 'fecha_uso') 
    
    search_fields = ('herramienta__serial', 'usuario__username', 'ubicacion')