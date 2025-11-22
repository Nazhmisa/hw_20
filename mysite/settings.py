"""
Django settings for mysite project.
"""

import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url
from django.urls import reverse_lazy  
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== БАЗОВЫЕ НАСТРОЙКИ ====================
DEBUG = config('DEBUG', default=False, cast=bool)

# Базовые разрешенные хосты
default_hosts = 'localhost,127.0.0.1,.onrender.com'
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=default_hosts, cast=Csv())

# Автоматически добавляем Render external hostname
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# В режиме DEBUG разрешаем все хосты для удобства разработки
if DEBUG:
    ALLOWED_HOSTS = ['*']
    print(f"⚠️  DEBUG MODE: ALLOWED_HOSTS set to {ALLOWED_HOSTS}")

# ==================== БЕЗОПАСНОЕ ПОЛУЧЕНИЕ SECRET_KEY ====================
def get_secret_key():
    """
    Безопасное получение SECRET_KEY:
    - Для collectstatic: временный случайный ключ
    - Для production: только из переменных окружения
    - Для разработки: временный ключ с предупреждением
    """
    # Проверяем, запущен ли collectstatic
    if os.environ.get('COLLECTSTATIC') == '1':
        temp_key = 'collectstatic-temp-key-' + get_random_secret_key()[:30]
        return temp_key
    
    # Получаем SECRET_KEY из переменных окружения
    secret_key = config('SECRET_KEY', default=None)
    
    # Если в production нет SECRET_KEY - падаем с ошибкой
    if not DEBUG and secret_key is None:
        raise ValueError(
            "SECRET_KEY not set in production. "
            "Please set SECRET_KEY environment variable."
        )
    
    # Если в разработке нет SECRET_KEY - используем временный с предупреждением
    if DEBUG and secret_key is None:
        temp_key = 'dev-temp-key-' + get_random_secret_key()[:30]
        print(f"⚠️  WARNING: Using temporary SECRET_KEY for development: {temp_key[:20]}...")
        print("⚠️  Please set SECRET_KEY in .env file for production!")
        return temp_key
    
    return secret_key

SECRET_KEY = get_secret_key()
# =========================================================================

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'debug_toolbar',
    'rest_framework',
    'django_filters',

    'shopapp.apps.ShopappConfig',
    'myauth.apps.MyauthConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Debug toolbar только в DEBUG режиме
if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# ==================== DATABASE ====================
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
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

# Internationalization
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = config('TIME_ZONE', default='UTC')
USE_I18N = True
USE_TZ = True

# ==================== STATIC & MEDIA FILES ====================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_REDIRECT_URL = reverse_lazy("myauth:about-me")
LOGIN_URL = reverse_lazy("myauth:login")

# ==================== SECURITY SETTINGS ====================
if not DEBUG:
    # Production security settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    # Development settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Debug Toolbar settings
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
        "0.0.0.0",
    ]
    
    # Автоматическое определение IP для Docker
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS.extend([ip[: ip.rfind(".")] + ".1" for ip in ips])

# ==================== LOGGING ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO' if DEBUG else 'WARNING',
    },
}