from rest_framework import serializers

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
            "term",
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
    school_fee = WriteSchoolFeeFKFieldSerializer()

    class Meta:
        model = SchoolFeesPayment
        exclude = (
            "uuid",
            "created_by",
            "created_at",
            "updated_at",
        )
