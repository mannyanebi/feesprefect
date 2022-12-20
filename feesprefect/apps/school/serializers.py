from rest_framework import serializers

from feesprefect.apps.school.models import AcademicClass, Student


class AcademicClassReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicClass
        exclude = (
            "created_by",
            "created_at",
            "updated_at",
        )


class AcademicClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicClass
        exclude = (
            "name",
            "created_by",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"id": {"read_only": False, "required": False}}


class StudentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = (
            "created_at",
            "updated_at",
        )
        lookup = "uuid"

    academic_class = AcademicClassReadSerializer()


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = (
            # "created_by",
            "created_at",
            "updated_at",
        )
        lookup = "uuid"

    academic_class = AcademicClassCreateSerializer(required=False)

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
