"""
URL configuration for intranetproject project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings 
from django.conf.urls.static import static 

# URL de tu frontend de React
# 🔁 CAMBIADO: de 'http://localhost:5173' a la IP que usas en la LAN
REACT_FRONTEND_URL = "http://192.168.0.40:5173/Intrafront/"

urlpatterns = [
    # 1. Rutas Administrativas de Django
    path("admin/", admin.site.urls),

    # 2. APIs de tu app 'login' (herramientas, registros de uso, auth, etc.)
    path("api/", include("login.urls")),

    # 3. Raíz del backend redirige al frontend de React
    path("", RedirectView.as_view(url=REACT_FRONTEND_URL, permanent=False)),
]

# ====================================================================
# CONFIGURACIÓN PARA SERVIR ARCHIVOS MULTIMEDIA EN DESARROLLO (DEBUG)
# ====================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

