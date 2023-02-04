# flake8: noqa

import os

from .base import *  # noqa

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================


# ==============================================================================
# CONFIG FOR RUNNING ON RENDER.COM
# ==============================================================================
# ALLOWED_HOSTS: List[str] = cast(List[str], config("ALLOWED_HOSTS", cast=Csv()))
ALLOWED_HOSTS: List[str] = []

print("BASE_DIR", BASE_DIR)

STATICFILES_DIRS = ["/opt/render/project/src/static"]
# print("STATICFILES_DIRS", STATICFILES_DIRS)

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
