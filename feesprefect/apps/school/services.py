from typing import List, Set

from django.db.models import QuerySet

from feesprefect.apps.school.models import AcademicClass, SchoolFee, SchoolFeesPayment


def sort_and_group_payments_by_school_fees(
    payments: QuerySet[SchoolFeesPayment],
) -> List[dict]:
    school_fees = SchoolFee.objects.filter(
        id__in=payments.values_list("school_fee", flat=True).distinct()
    )

    academic_classes: Set[AcademicClass] = set(
        school_fee.academic_class for school_fee in school_fees
    )

    school_fees_payments_in_academic_class = [
        (
            academic_class,
            [
                (school_fee, payments.filter(school_fee=school_fee))
                for school_fee in school_fees.filter(academic_class=academic_class)
            ],
        )
        for academic_class in academic_classes
    ]

    school_fees_payments_details = []
    for academic_class, school_fees_payments in school_fees_payments_in_academic_class:
        for school_fee, payments_for_school_fee in school_fees_payments:
            school_fees_payments_details.append(
                {
                    "academic_class_name": academic_class.name,
                    "payments": [
                        {
                            "school_fee_name": f"{school_fee.session.name}  - {school_fee.session.term}",  # pylint: disable=line-too-long
                            "school_fee_amount": school_fee.amount,
                            "payments": payments_for_school_fee.values_list(
                                "amount_paid", "is_registration_fee_payment", named=True
                            ),
                            "is_payment_complete": any(
                                payment_for_school_fee.is_payment_complete
                                for payment_for_school_fee in payments_for_school_fee
                            ),
                        }
                    ],
                }
            )
    return school_fees_payments_details
