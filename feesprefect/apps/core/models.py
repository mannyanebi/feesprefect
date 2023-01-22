import uuid

from django.db import models


# Create your models here.
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
