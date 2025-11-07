from django.apps import AppConfig

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

    # ESTA FUNCIÓN FUERZA LA CARGA DE LAS SEÑALES
    def ready(self):
        # Importamos el archivo models.py para que se registren los @receiver
        import login.models
