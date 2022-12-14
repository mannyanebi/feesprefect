from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from moneyed.classes import NGN

from feesprefect.apps.core.models import TimestampMixin

# Create your models here.


class Student(TimestampMixin, models.Model):
    name = models.CharField(_("Student Name"), max_length=255, blank=False, null=False)
    academic_class = models.ForeignKey(
        "school.AcademicClass",
        verbose_name=_("Academic Class"),
        on_delete=models.CASCADE,
        related_name="students",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="students_created",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class AcademicClass(TimestampMixin, models.Model):
    name = models.CharField(_("Class Name"), max_length=255, blank=False, null=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="classes_created",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Academic class"
        verbose_name_plural = "Academic classes"


FIRST_TERM = "First Term"
SECOND_TERM = "Second Term"
THIRD_TERM = "Third Term"

TERM_CHOICES = (
    ("first-term", FIRST_TERM),
    ("second-term", SECOND_TERM),
    ("third-term", THIRD_TERM),
)


class AcademicSession(TimestampMixin, models.Model):
    name = models.CharField(_("Session Name"), max_length=255, blank=False, null=False)
    term = models.CharField(
        _("Academic Term"), max_length=50, choices=TERM_CHOICES, default=FIRST_TERM
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="academic_sessions_created",
    )

    class Meta:
        verbose_name = "Academic session"
        verbose_name_plural = "Academic sessions"


class SchoolFee(TimestampMixin, models.Model):
    amount = MoneyField(
        max_digits=14, decimal_places=2, null=False, blank=False, default_currency=NGN
    )  # type: ignore
    academic_class = models.ForeignKey(
        "school.AcademicClass",
        verbose_name=_("Academic Class"),
        on_delete=models.CASCADE,
        related_name="school_fees",
    )
    session = models.ForeignKey(
        "school.AcademicSession",
        verbose_name=_("Academic Session"),
        on_delete=models.CASCADE,
        related_name="school_fees",
    )
    term = models.CharField(
        _("Academic Term"), max_length=50, choices=TERM_CHOICES, default=FIRST_TERM
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="school_fees_created",
    )

    def __str__(self):
        return f"{self.academic_class.name} {self.session.name}"

    class Meta:
        verbose_name = "School fee"
        verbose_name_plural = "School fees"


class SchoolFeesPayment(TimestampMixin, models.Model):
    student = models.ForeignKey(
        "school.Student",
        verbose_name=_("Student"),
        on_delete=models.CASCADE,
        related_name="school_fees_payments",
    )
    amount_paid = MoneyField(
        max_digits=14, decimal_places=2, null=True, blank=True, default_currency=NGN
    )  # type: ignore
    school_fee = models.ForeignKey(
        "school.SchoolFee",
        verbose_name=_("School Fee"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="payments",
    )
    is_payment_complete = models.BooleanField(_("Is Payment Completed?"), default=False)
    payment_date = models.DateField(
        _("Payment Date"), auto_now=True, auto_now_add=False
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="school_fees_payments_created",
    )

    def __str__(self):
        return self.student.name

    class Meta:
        verbose_name = "School fees payment"
        verbose_name_plural = "School fees payments"
