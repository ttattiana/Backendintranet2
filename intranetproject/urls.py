"""
URL configuration for intranetproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
# 🛑 NUEVAS IMPORTACIONES para manejar archivos multimedia
from django.conf import settings 
from django.conf.urls.static import static 


# Define la URL de tu frontend de React
REACT_FRONTEND_URL = 'http://localhost:5173' 

urlpatterns = [
    # 1. Rutas Administrativas de Django
    path('admin/', admin.site.urls),

    # 2. Incluye todas las rutas definidas en tu app login (incluye APIs)
    path('api/', include('login.urls')), # ✅ Sugerencia: Usa un prefijo 'api/' para mejor organización

    # 3. ÚLTIMO RECURSO: Redirige la raíz (/) al Frontend de React
    path('', RedirectView.as_view(url=REACT_FRONTEND_URL, permanent=False)), 
]

# ====================================================================
# CONFIGURACIÓN PARA SERVIR ARCHIVOS MULTIMEDIA EN DESARROLLO (DEBUG)
# ====================================================================
# Esta configuración permite que Django sirva las fotos subidas.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
