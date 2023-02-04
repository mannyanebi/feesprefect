from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from feesprefect.apps.school.resources import StudentResource

from . import models

# Register your models here.


@admin.register(models.Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "academic_class",
        "created_by",
    )
    list_filter = ("academic_class",)
    search_fields = ("academic_class__name",)
    readonly_fields = ("uuid",)
    resource_classes = (StudentResource,)


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
        "term",
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
    readonly_fields = ("uuid",)
