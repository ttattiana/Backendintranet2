from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# IMPORTACIÓN CLAVE: Importamos las señales Y los modelos
from .models import Herramienta, Profile, create_user_profile, save_user_profile 


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
    # Controla la visibilidad del inline: solo en vista de edición.
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

    # Asegura que el inline solo se muestre si el objeto User YA existe (obj is not None).
    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return [] 
        return super().get_inline_instances(request, obj)

    # 🛑 SOLUCIÓN INTEGRAL para IntegrityError (al crear el User)
    def save_model(self, request, obj, form, change):
        # 1. Desconecta ambas señales ANTES de guardar el User.
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)
        
        try:
            # 2. Guarda el objeto User principal (disparando la creación del Profile por el Admin)
            super().save_model(request, obj, form, change)
            
            # 3. Si es NUEVO, creamos el perfil MANUALMENTE (solo si la señal está desconectada).
            if not change:
                # Usamos create() para asegurar que el perfil exista
                Profile.objects.create(user=obj) 
        finally:
            # 4. Reconecta ambas señales SIEMPRE.
            post_save.connect(create_user_profile, sender=User)
            post_save.connect(save_user_profile, sender=User)
            
    # 🛑 ELIMINADA: La función save_formset se elimina para resolver el AttributeError.

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