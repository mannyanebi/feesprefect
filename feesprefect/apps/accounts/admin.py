# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

# @admin.register(models.GeneralSettings)
# class GeneralSettingsAdmin(admin.ModelAdmin):
#     list_display = (
#         "preferred_payment_gateway",
#         "default_transaction_fee_percentage",
#     )


@admin.register(models.FeesprefectAdmin)
class FeesprefectUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )
    ordering = ["-date_joined"]
