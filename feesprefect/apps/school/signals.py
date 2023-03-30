# from django.db.models.signals import pre_save
# from feesprefect.apps.core.serializers import MoneyFieldSerializer
# from django.dispatch import receiver

# from feesprefect.apps.school.models import SchoolFeesPayment


# @receiver(pre_save, sender=SchoolFeesPayment)
# def update_school_fee_payment_is_payment_complete_field(
#     sender, instance: SchoolFeesPayment, **kwargs  # pylint: disable=unused-argument
# ):
#     serialized_school_fee_amount = MoneyFieldSerializer(instance.school_fee.amount).data  # type: ignore
#     original_school_fee_amount = float(serialized_school_fee_amount["amount"])

#     serialized_amount_paid = MoneyFieldSerializer(instance.amount_paid).data
#     amount_paid = float(serialized_amount_paid["amount"])

#     print("original_school_fee_amount", original_school_fee_amount)
#     print("amount_paid", amount_paid)
#     print("amount_paid < original_school_fee_amount", amount_paid < original_school_fee_amount)

#     if amount_paid < original_school_fee_amount:
#         instance.is_payment_complete = False
#     else:
#         instance.is_payment_complete = True
