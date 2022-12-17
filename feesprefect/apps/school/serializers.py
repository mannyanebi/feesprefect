from rest_framework import serializers

from feesprefect.apps.school.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = (
            "created_at",
            "updated_at",
        )
        lookup = "uuid"
