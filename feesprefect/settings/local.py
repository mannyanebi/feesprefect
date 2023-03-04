# Monkey patching with Django Stubs
import django_stubs_ext

from .base import *  # noqa, pylint: disable=wildcard-import, unused-wildcard-import

django_stubs_ext.monkeypatch()


INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "feesprefect.local.sqlite3",
    }
}
