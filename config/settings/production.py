from os import path, getenv
from dotenv import load_dotenv

from .base import * #noqa
from .base import BASE_DIR

prod_env_file = path.join(BASE_DIR, ".envs", "env.production")

if path.isfile(prod_env_file):
    load_dotenv(prod_env_file)


SECRET_KEY = getenv("DJANGO_SECRET_KEY")

ADMIN_URL = getenv("DJANGO_ADMIN_URL")

ALLOWED_HOSTS = [".onrender.com"]

ADMINS=[("Jorge Calleros", "calleros.dev@gmail.com"),]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("SMTP_MAILGUN_PASSWORD")
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = getenv("DEFAULT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")

CORS_ALLOWED_ORIGINS=["https://vetmanagementwebclient.onrender.com"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = getenv("DJANGO_SECURE_SSL_REDIRECT", "True") == "True"


COOKIE_NAME="access"
COOKIE_SAMESITE="None"
COOKIE_PATH="/"
COOKIE_HTTPONLY = True
COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ["https://www.vetmanagementwebclient.onrender.com", "https://vetmanagementwebclient.onrender.com"]
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}