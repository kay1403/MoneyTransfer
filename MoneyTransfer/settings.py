from pathlib import Path
import os
import dj_database_url
import urllib.parse
import environ
from datetime import timedelta

# ------------------------
# Base directory
# ------------------------
#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------
# Charger le .env
# ------------------------
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ------------------------
# Sécurité et debug
# ------------------------
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = [
    "moneytransfer-db23.onrender.com",
    "moneytransfer.onrender.com",
    "127.0.0.1",
    "localhost"
]

# ------------------------
# Applications installées
# ------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'core',
    'accounts',
    'transactions',
    'channels',
]

AUTH_USER_MODEL = 'accounts.User'
ASGI_APPLICATION = "MoneyTransfer.asgi.application"

# ------------------------
# Redis / Channels
# ------------------------
redis_url = env('REDIS_URL', default='redis://127.0.0.1:6379')
parsed_url = urllib.parse.urlparse(redis_url)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(parsed_url.hostname, parsed_url.port)],
            "password": parsed_url.password,
            "ssl": parsed_url.scheme == "rediss",
        },
    },
}

# ------------------------
# REST Framework
# ------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ------------------------
# Middleware
# ------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://moneytransfergr.netlify.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://moneytransfergr.netlify.app"
]

# ------------------------
# HTTPS & sécurité cookies
# ------------------------
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

ROOT_URLCONF = 'MoneyTransfer.urls'

# ------------------------
# Templates
# ------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'money-transfer-frontend', 'dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MoneyTransfer.wsgi.application'

# ------------------------
# Database PostgreSQL externe
# ------------------------
DATABASES = {
    'default': dj_database_url.parse(
        env('DATABASE_URL'),
        conn_max_age=600
    )
}

# ------------------------
# Validation des mots de passe
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------
# Internationalisation
# ------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------
# Static & Media
# ------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'money-transfer-frontend', 'dist'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------
# Logging production
# ------------------------
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    try:
        os.makedirs(LOG_DIR)
    except PermissionError:
        # Sur Render ou autre plateforme read-only, utiliser /tmp
        LOG_DIR = '/tmp'

LOG_FILE = os.path.join(LOG_DIR, 'django.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],  # log à la fois dans le fichier et la console
            'level': 'INFO',
            'propagate': True,
        },
    },
}