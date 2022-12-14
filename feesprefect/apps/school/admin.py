from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "academic_class",
        "created_by",
    )


@admin.register(models.AcademicClass)
class AcademicClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_by",
    )


@admin.register(models.AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "term",
        "created_by",
    )


@admin.register(models.SchoolFee)
class SchoolFeeAdmin(admin.ModelAdmin):
    list_display = (
        "academic_class",
        "session",
        "amount",
    )


@admin.register(models.SchoolFeesPayment)
class SchoolFeesPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "amount_paid",
        "school_fee",
        "is_payment_complete",
    )
