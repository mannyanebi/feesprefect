from rest_framework import viewsets

from feesprefect.apps.school.models import Student
from feesprefect.apps.school.pagination import StudentsListPagination
from feesprefect.apps.school.serializers import StudentSerializer

# Create your views here.


class StudentViewSet(viewsets.ModelViewSet):
    """
    The Student ModelViewSet with all CRUD actions. We prefer to use UUID field for lookup
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StudentsListPagination
    lookup_field = "uuid"
    # lookup_value_regex = r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$" # pylint: disable=line-too-long
