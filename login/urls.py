from django.urls import path
from .views import (
    login_view, verify_otp, register_view,
    registrar_herramienta, registrar_uso,
    ver_detalle_uso_seguro, listar_registros_uso
)

urlpatterns = [
    # Rutas de Autenticación
    path('login/', login_view, name='login_view'), 
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('register/', register_view, name='register_view'),
    
    # Rutas de Herramientas
    path('herramienta/registrar/', registrar_herramienta, name='registrar_herramienta'),
    path('herramienta/uso/', registrar_uso, name='registrar_uso'),
    path('herramienta/uso/detalle/<int:id>/', ver_detalle_uso_seguro, name='ver_detalle_uso_seguro'),
    
    # Nuevo endpoint para listar registros de uso (todos)
    path('uso/', listar_registros_uso, name='listar_registros_uso'),
]
