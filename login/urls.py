from django.urls import path
# Asegúrate de que todas estas vistas estén importadas correctamente
from .views import login_view, verify_otp, register_view, registrar_herramienta, registrar_uso, ver_detalle_uso_seguro 

urlpatterns = [
    # Rutas de Autenticación
    path('login/', login_view, name='login_view'), 
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('register/', register_view, name='register_view'),
    
    # Rutas de Herramientas
    # RUTA DE REGISTRO DE NUEVA HERRAMIENTA
    path('herramienta/registrar/', registrar_herramienta, name='registrar_herramienta'),
    
    # RUTA: Para registrar el uso/escaneo
    path('herramienta/uso/', registrar_uso, name='registrar_uso'), 
    
    # 🎯 CORRECCIÓN CLAVE: Cambiamos '<int:registro_id>' a '<int:id>' 
    # para que coincida con el parámetro que usa tu función 'ver_detalle_uso_seguro(request, id)'.
    path('herramienta/uso/detalle/<int:id>/', ver_detalle_uso_seguro, name='ver_detalle_uso_seguro'),
]