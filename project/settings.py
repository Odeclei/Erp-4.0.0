# Flake8: noqa

import json
import os

from django.contrib.messages import constants as messages
from getmac import get_mac_address as gma

# from unittest import expectedFailure


MESSAGE_TAGS = {
    messages.ERROR: "danger",
    messages.INFO: "info",
    messages.WARNING: "warning",
    messages.DEBUG: "secondary",
    messages.SUCCESS: "success",
}


def add_mac(mac):
    try:
        with open("macs.json", "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = []
    if mac not in dados:
        dados.append(mac)
    with open("macs.json", "w") as f:
        json.dump(dados, f, indent=4)


add_mac(gma())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(RAIZ_DIR, "data", "web")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-l**6e-@kxojjvqt#j%pi^++x%h8k*1!v=ue7r5ene@sjx6@m!x'
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # my apps
    "rule",
    "cad_item",
    "apont",
    "desempenho",
    "site_setup",
    "ppcp",
    "dashboard",
    "carregamento",
    "clientes",
    # third aps
    "rest_framework",
]

# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # my middleware
    # 'site_setup.turno_middleware.GlobalSettingsMiddleware'
]


ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(RAIZ_DIR, "base_templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "site_setup.context_processor.site_setup",
                "site_setup.context_processor.horario_turnos",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(RAIZ_DIR, "db.sqlite3"),
    },
}

"""
        'ENGINE': os.getenv('DB_ENGINE', 'change-me'),
        'NAME': os.getenv('POSTGRES_DB', 'change-me'),
        'USER': os.getenv('POSTGRES_USER', 'change-me'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'change-me'),
        'HOST': os.getenv('POSTGRES_HOST', 'change-me'),
        'PORT': os.getenv('POSTGRES_PORT', 'change-me'),
"""
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATIC_ROOT = os.path.join(RAIZ_DIR, "static")
MEDIA_ROOT = os.path.join(RAIZ_DIR, "media")


STATICFILES_DIRS = [
    os.path.join(RAIZ_DIR, "base_static"),
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure the logs directory exists

LOGOUT_REDIRECT_URL = "site_setup:index"

LOGIN_REDIRECT_URL = "/home/"
LOGIN_URL = "/login/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "json_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django_json.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "json",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            # You can choose to log to console and file
            "handlers": ["json_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "site_setup": {  # Replace 'myapp' with the name of your Django app
            "handlers": ["json_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "": {  # Root logger - catches everything not caught by more specific loggers
            "handlers": ["json_file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
