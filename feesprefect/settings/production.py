# flake8: noqa

import os

from .base import *  # noqa, pylint: disable=wildcard-import, unused-wildcard-import

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================


# ==============================================================================
# Config for Serving Static Files
# ==============================================================================
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "feesprefect.sqlite3",
#     }
# }

# ==============================================================================
# CONFIG FOR RUNNING ON RENDER.COM
# ==============================================================================

# ALLOWED_HOSTS: List[str] = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
