from django.contrib.auth.models import AbstractUser


# Create your models here.
class FeesprefectAdmin(AbstractUser):
    pass  # pylint: disable=unnecessary-pass

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Feesprefect Admin"
        verbose_name_plural = "Feesprefect Admins"
