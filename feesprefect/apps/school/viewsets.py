from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework import exceptions, viewsets

from feesprefect.apps.school.models import AcademicClass, Student
from feesprefect.apps.school.pagination import StudentsListPagination
from feesprefect.apps.school.serializers import (
    AcademicClassReadSerializer,
    StudentCreateSerializer,
    StudentReadSerializer,
)

# Create your views here.


class StudentViewSet(viewsets.ModelViewSet):
    """
    The Student ModelViewSet with all CRUD actions. We prefer to use UUID field for lookup
    """

    queryset = Student.objects.all()
    pagination_class = StudentsListPagination
    lookup_field = "uuid"
    renderer_classes = [CamelCaseJSONRenderer]
    # lookup_value_regex = r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$" # pylint: disable=line-too-long

    def get_serializer_class(self):
        try:
            assert self.request.method is not None
            if self.action in ("list", "retrieve"):
                return StudentReadSerializer
            return StudentCreateSerializer
        except AssertionError as request_method_error:
            raise exceptions.APIException(
                detail="Request Method not Found"
            ) from request_method_error


class AcademicClassViewSet(viewsets.ModelViewSet):
    """
    The Student ModelViewSet with all CRUD actions. We prefer to use UUID field for lookup
    """

    queryset = AcademicClass.objects.all()
    serializer_class = AcademicClassReadSerializer
