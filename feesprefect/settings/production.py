# flake8: noqa

import os

from .base import *  # noqa

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================


# ==============================================================================
# Config for Serving Static Files
# ==============================================================================
MIDDLEWARE.insert(3, "whitenoise.middleware.WhiteNoiseMiddleware")

# ==============================================================================
# CONFIG FOR RUNNING ON RENDER.COM
# ==============================================================================

ALLOWED_HOSTS: List[str] = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
