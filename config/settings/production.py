from os import path, getenv
from dotenv import load_dotenv

from .base import * #noqa
from .base import BASE_DIR

prod_env_file = path.join(BASE_DIR, ".envs", "env.production")

if path.isfile(prod_env_file):
    load_dotenv(prod_env_file)


SECRET_KEY = getenv("DJANGO_SECRET_KEY")

ADMIN_URL = getenv("DJANGO_ADMIN_URL")

ALLOWED_HOSTS = ["vetmanagementapi.onrender.com"]

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

LOGGING = {
    "version": 1, 
    "disable_existing_loggers": False, 
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers":{
        "console": {
            "level":"DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    },
}