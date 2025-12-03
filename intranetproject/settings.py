"""
Django settings for intranetproject project.
"""

from pathlib import Path
from corsheaders.defaults import default_headers 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-8yk@6+08e3q@+mjkf1@lk(1qkv%+qop3s9&0=@1qs+vosp%=^g'

DEBUG = True

# 🛑 SOLUCIÓN A CONEXIÓN Y DISALLOWEDHOST 🛑
# Hemos añadido tu IP de red actual (192.168.0.40) para que Django confíe en ella.
ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    '192.168.0.40', # <--- ¡TU IP ACTUAL!
    '*'
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'login',
    'rest_framework',
    'corsheaders', 
]

MIDDLEWARE = [
    # CORS debe estar al inicio para funcionar correctamente.
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'intranetproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'intranetproject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ------------------- CONFIGURACIÓN CORS CORREGIDA -------------------
# Añadimos la IP actual de tu PC (192.168.0.40) y el puerto de VITE (5173).
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://192.168.0.40:5173", # <--- ¡CLAVE! Permite al frontend acceder al backend
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Content-Type',
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------- CONFIGURACIÓN MEDIA (ARCHIVOS) -------------------
MEDIA_ROOT = BASE_DIR / 'media' 
MEDIA_URL = '/media/'