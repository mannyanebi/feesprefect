import os

from decouple import config


def set_environment():
    FEESPREFECT_ENVIRONMENT = config(  # pylint: disable = invalid-name
        "FEESPREFECT_ENVIRONMENT", default="local"
    )

    ENVIRONMENT_MODULE = f"feesprefect.settings.{FEESPREFECT_ENVIRONMENT}"  # pylint: disable = invalid-name

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", ENVIRONMENT_MODULE)
