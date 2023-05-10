# flake8: noqa

import os

import dj_database_url
from decouple import config

from .base import *  # noqa, pylint: disable=wildcard-import, unused-wildcard-import

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================


# ==============================================================================
# Config for Serving Static Files
# ==============================================================================
MIDDLEWARE.insert(3, "whitenoise.middleware.WhiteNoiseMiddleware")

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "feesprefect.sqlite3",
#     }
# }

DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")

DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
}

# ==============================================================================
# CONFIG FOR RUNNING ON RENDER.COM
# ==============================================================================

ALLOWED_HOSTS: List[str] = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
