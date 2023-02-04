from django.db.models.signals import pre_save
from django.dispatch import receiver

from feesprefect.apps.school.models import SchoolFeesPayment


@receiver(pre_save, sender=SchoolFeesPayment)
def update_school_fee_payment_is_payment_complete_field(
    sender, instance: SchoolFeesPayment, **kwargs  # pylint: disable=unused-argument
):
    original_school_fee_amount = instance.school_fee.amount  # type: ignore
    if instance.amount_paid <= original_school_fee_amount:
        instance.is_payment_complete = False
    else:
        instance.is_payment_complete = True
