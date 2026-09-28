"""
Django settings for config project.
"""

import os
import sys
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core security settings -------------------------------------------------

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-x=f71$0kecf%%r2nr%n0nsxqbu*rl#zf4rvk)l*8utf-zc*1)g',
)

# Debug mode is ON only when you start the project with `manage.py runserver`
# on your own computer. Anywhere else (Railway, Render, Vercel...) it is OFF,
# unless you deliberately set DEBUG=True in the environment.
ON_HOSTING_PLATFORM = bool(os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER'))
_debug_env = os.environ.get('DEBUG')
DEBUG = (_debug_env == 'True') if _debug_env is not None else ('runserver' in sys.argv)

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()
]

# Railway/Render give you a public domain via this env var (Railway) or you
# set it yourself (Render). Add it automatically so ALLOWED_HOSTS doesn't
# break deploys.
RAILWAY_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)

RENDER_DOMAIN = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_DOMAIN:
    ALLOWED_HOSTS.append(RENDER_DOMAIN)

if ON_HOSTING_PLATFORM:
    # Railway/Render terminate HTTPS at their proxy; tell Django to trust it.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [f'https://{h}' for h in ALLOWED_HOSTS if h not in ('127.0.0.1', 'localhost')]


# --- Applications -------------------------------------------------------------

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channels',

    'accounts',
    'orders',
    'chatapp',
]

AUTH_USER_MODEL = 'accounts.User'

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'


# --- Channels (WebSockets for chat) -------------------------------------------

REDIS_URL = os.environ.get('REDIS_URL')

if REDIS_URL:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
else:
    # Falls back to in-memory layer for local dev without Redis running.
    # Fine for a single process; NOT fine for production (won't work across
    # multiple server workers). Set REDIS_URL before deploying.
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }


# --- Database -------------------------------------------------------------

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# --- Password validation -------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internationalization -------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static files -------------------------------------------------------

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}


# --- Auth redirects -------------------------------------------------------

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'orders:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'