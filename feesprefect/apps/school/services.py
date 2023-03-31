from typing import List, Tuple

from django.db.models import QuerySet

from feesprefect.apps.school.models import SchoolFee, SchoolFeesPayment


def sort_and_group_payments_by_school_fees(
    payments: QuerySet[SchoolFeesPayment],
) -> List[dict]:
    school_fees = SchoolFee.objects.filter(
        id__in=payments.values_list("school_fee", flat=True).distinct()
    )

    school_fees_payments: List[Tuple[SchoolFee, QuerySet[SchoolFeesPayment]]] = []
    for school_fee in school_fees:
        payments_for_school_fee = payments.filter(school_fee=school_fee)
        school_fees_payments.append((school_fee, payments_for_school_fee))

    school_fees_payments_details = []
    for school_fee, payments_for_school_fee in school_fees_payments:
        school_fees_payments_details.append(
            {
                "school_fee_name": f"{school_fee.session.name}  - {school_fee.session.term}",
                "school_fee_amount": school_fee.amount,
                "payments": payments_for_school_fee.values_list(
                    "amount_paid", flat=True
                ),
                "is_payment_complete": any(
                    payment_for_school_fee.is_payment_complete
                    for payment_for_school_fee in payments_for_school_fee
                ),
            }
        )

    return school_fees_payments_details
