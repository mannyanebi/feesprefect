from django.db.models import Sum
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers
from rest_framework.exceptions import APIException, NotFound, ValidationError

from feesprefect.apps.school.models import (
    AcademicClass,
    AcademicSession,
    SchoolFee,
    SchoolFeesPayment,
    Student,
)


class AcademicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicClass
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )


class WriteAcademicClassFKFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicClass
        exclude = (
            "name",
            "created_by",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"id": {"read_only": False, "required": False}}


class ReadStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )
        lookup = "uuid"

    academic_class = AcademicClassSerializer()


class WriteStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )
        lookup = "uuid"

    academic_class = WriteAcademicClassFKFieldSerializer()

    def create(self, validated_data):
        # hook and intercept the validated_data to fetch the Academic Class model object
        try:

            academic_class = validated_data.pop("academic_class")
            academic_class_obj = AcademicClass.objects.get(id=academic_class.get("id"))
            instance = Student.objects.create(
                academic_class=academic_class_obj, **validated_data
            )
            return instance

        except AcademicClass.DoesNotExist as does_not_exist:
            raise serializers.ValidationError(
                {"academic_class": "Invalid academic_class Id"}
            ) from does_not_exist


class WriteStudentFKFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = (
            "id",
            "name",
            "academic_class",
            "created_by",
        )

        extra_kwargs = {"uuid": {"read_only": False}}


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )


class WriteAcademicSessionFKFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        exclude = (
            "name",
            "term",
            "created_by",
            "created_at",
            "updated_at",
        )

        extra_kwargs = {"id": {"read_only": False}}


class WriteSchoolFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFee
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )

    academic_class = WriteAcademicClassFKFieldSerializer()
    session = WriteAcademicSessionFKFieldSerializer()

    def create(self, validated_data):
        # hook and intercept the validated_data to fetch the Academic Class model object
        try:

            academic_class = validated_data.pop("academic_class")
            academic_session = validated_data.pop("session")
            academic_class_obj = AcademicClass.objects.get(id=academic_class.get("id"))
            academic_session_obj = AcademicSession.objects.get(
                id=academic_session.get("id")
            )
            instance = SchoolFee.objects.create(
                academic_class=academic_class_obj,
                session=academic_session_obj,
                **validated_data
            )
            return instance

        except AcademicClass.DoesNotExist as does_not_exist:
            raise serializers.ValidationError(
                {"academic_class": "Invalid academic_class Id"}
            ) from does_not_exist

        except AcademicSession.DoesNotExist as does_not_exist:  # type: ignore
            raise serializers.ValidationError(
                {"session_": "Invalid session (academic_session) Id"}
            ) from does_not_exist


class WriteSchoolFeeFKFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFee
        exclude = (
            "amount",
            "academic_class",
            "session",
            "created_by",
            "created_at",
            "updated_at",
        )

        extra_kwargs = {"id": {"read_only": False}}


class ReadSchoolFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolFee
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )

    academic_class = AcademicClassSerializer()
    session = AcademicSessionSerializer()


class ReadSchoolFeesPaymentSerializer(serializers.ModelSerializer):
    student = ReadStudentSerializer()
    school_fee = ReadSchoolFeeSerializer()

    class Meta:
        model = SchoolFeesPayment
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )
        lookup_field = "uuid"


class WriteSchoolFeesPaymentSerializer(serializers.ModelSerializer):
    student = WriteStudentFKFieldSerializer()
    amount_paid = MoneyField(max_digits=14, decimal_places=2)
    school_fee = WriteSchoolFeeFKFieldSerializer()

    class Meta:
        model = SchoolFeesPayment
        exclude = (
            "uuid",
            # "school_fee",
            "is_payment_complete",
            "created_by",
            "created_at",
            "updated_at",
        )

        extra_kwargs = {"amount_paid": {"required": True}}

    def create(self, validated_data):
        try:
            student = validated_data.pop("student")
            school_fee = validated_data.pop("school_fee")
            student_obj = Student.objects.select_related("academic_class").get(
                uuid=student["uuid"]
            )
            school_fee_obj = SchoolFee.objects.get(
                id=school_fee["id"], academic_class_id=student_obj.academic_class.id
            )

            # We want to check if a previous payment has been made for this student
            # and if so, we want to get the previous amounts paid, add the new amount
            # and check if the new total is less than or equal to the school fee amount
            # we want to return is_payment_complete as true

            previous_payments = SchoolFeesPayment.objects.filter(
                student_id=student_obj.id,  # type: ignore
                school_fee_id=school_fee["id"],  # type: ignore
            ).order_by("-created_at")

            if previous_payments.exists():
                total_amounts_of_previous_payments = previous_payments.aggregate(
                    total_previous_amounts=Sum("amount_paid")
                )
                total_amounts_of_previous_payments = int(
                    total_amounts_of_previous_payments.get("total_previous_amounts", 0)
                )
                new_amount_paid = (
                    total_amounts_of_previous_payments + validated_data["amount_paid"]
                )

                if new_amount_paid <= school_fee_obj.amount.amount:
                    if new_amount_paid == school_fee_obj.amount.amount:
                        validated_data.update(
                            {
                                "student": student_obj,
                                "school_fee": school_fee_obj,
                                "is_payment_complete": True,
                            }
                        )
                    validated_data.update(
                        {
                            "student": student_obj,
                            "school_fee": school_fee_obj,
                            "is_payment_complete": False,
                        }
                    )

                    school_fee_payment = SchoolFeesPayment.objects.create(
                        **validated_data
                    )
                    return school_fee_payment
                else:
                    raise ValidationError(
                        "The amount paid plus previous amounts is greater than the \
                          original school fee amount"
                    )
            else:
                # This is the first payment for this student
                validated_data.update(
                    {"student": student_obj, "school_fee": school_fee_obj}
                )

                school_fee_payment = SchoolFeesPayment.objects.create(**validated_data)
                return school_fee_payment
        except Student.DoesNotExist as student_not_found:
            raise NotFound("Student not found") from student_not_found

    def update(self, instance: SchoolFeesPayment, validated_data):
        if "student" in validated_data:
            raise ValidationError("You can't update the student field for this record")
        amount_paid = validated_data.pop("amount_paid")

        school_fee: SchoolFee = instance.student.academic_class.school_fees.get(
            academic_class_id=instance.student.academic_class.id
        )
        new_amount_paid = instance.amount_paid.amount + amount_paid

        if new_amount_paid <= school_fee.amount.amount:
            instance.amount_paid = new_amount_paid
        else:
            raise APIException(
                detail="New total amount paid cannot be more than school fee total amount"
            )

        return super().update(instance, validated_data)
