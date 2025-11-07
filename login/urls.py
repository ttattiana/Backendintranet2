from django.urls import path
# 🛑 IMPORTACIÓN ACTUALIZADA: Asegúrate de incluir registrar_uso
from .views import login_view, verify_otp, register_view, registrar_herramienta, registrar_uso 

urlpatterns = [
    # Rutas de Autenticación
    # Añadimos / al final por consistencia con RESTful y el resto del proyecto
    path('login/', login_view, name='login_view'), 
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('register/', register_view, name='register_view'),
    
    # Rutas de Herramientas
    # RUTA DE REGISTRO DE NUEVA HERRAMIENTA (con foto inicial)
    path('herramienta/registrar/', registrar_herramienta, name='registrar_herramienta'),
    
    # 🛑 NUEVA RUTA: Para registrar el uso/escaneo (con foto de evidencia)
    path('herramienta/uso/', registrar_uso, name='registrar_uso'), 
]
