from django_filters import rest_framework as filters

from feesprefect.apps.school.models import Student


class StudentFilter(filters.FilterSet):
    name__contains = filters.CharFilter(field_name="name", lookup_expr="contains")

    class Meta:
        model = Student
        fields = [
            "academic_class_id",
        ]
