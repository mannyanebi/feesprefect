#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from decouple import config


def main():
    IS_FEESPREFECT_PROD_ENVIRONMENT = config(  # pylint: disable = invalid-name
        "IS_FEESPREFECT_PROD_ENVIRONMENT", default=False, cast=bool
    )

    """Run administrative tasks."""

    if IS_FEESPREFECT_PROD_ENVIRONMENT:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "feesprefect.settings.production"
        )
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feesprefect.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
