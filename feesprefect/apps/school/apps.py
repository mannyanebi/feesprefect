from django.apps import AppConfig


class SchoolConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feesprefect.apps.school"

    def ready(self):
        import feesprefect.apps.school.signals  # noqa # pylint: disable=unused-import
