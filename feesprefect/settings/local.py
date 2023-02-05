# Monkey patching with Django Stubs
import django_stubs_ext

from .base import *  # noqa, pylint: disable=wildcard-import, unused-wildcard-import

django_stubs_ext.monkeypatch()


INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# STATICFILES_DIRS = [BASE_DIR / "static"]

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
