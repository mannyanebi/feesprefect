from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, viewsets

from feesprefect.apps.school.filters import StudentFilter
from feesprefect.apps.school.mixins import PerformCreateWithAdmin
from feesprefect.apps.school.models import (
    AcademicClass,
    AcademicSession,
    SchoolFee,
    SchoolFeesPayment,
    Student,
)
from feesprefect.apps.school.pagination import ListPagination
from feesprefect.apps.school.serializers import (
    AcademicClassSerializer,
    AcademicSessionSerializer,
    ReadSchoolFeeSerializer,
    ReadSchoolFeesPaymentSerializer,
    ReadStudentSerializer,
    WriteSchoolFeeSerializer,
    WriteSchoolFeesPaymentSerializer,
    WriteStudentSerializer,
)

# Create your views here.


class StudentViewSet(PerformCreateWithAdmin, viewsets.ModelViewSet):
    """
    The Student ModelViewSet with all CRUD actions. We prefer to use UUID field for lookup
    """

    queryset = Student.objects.all().order_by("id")
    pagination_class = ListPagination
    lookup_field = "uuid"
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    # filterset_fields = ["academic_class_id", "name__contains"]
    # lookup_value_regex = r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$" # pylint: disable=line-too-long

    def paginate_queryset(self, queryset):
        if "all" in self.request.query_params:  # type: ignore
            return None
        return super().paginate_queryset(queryset)

    def get_serializer_class(self):
        try:
            assert self.request.method is not None
            if self.action in ("list", "retrieve"):
                return ReadStudentSerializer
            return WriteStudentSerializer
        except AssertionError as request_method_error:
            raise exceptions.APIException(
                detail="Request Method not Found"
            ) from request_method_error


class AcademicClassViewSet(PerformCreateWithAdmin, viewsets.ModelViewSet):
    """
    The Academic Class ModelViewSet with all CRUD actions. We prefer to use id field for lookup
    """

    queryset = AcademicClass.objects.all()
    serializer_class = AcademicClassSerializer


class AcademicSessionViewSet(PerformCreateWithAdmin, viewsets.ModelViewSet):
    """
    The Academic Class ModelViewSet with all CRUD actions. We prefer to use id field for lookup
    """

    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer


class SchoolFeesViewSet(PerformCreateWithAdmin, viewsets.ModelViewSet):
    """
    The School Fee ModelViewSet with all CRUD actions. We prefer to use id field for lookup
    """

    queryset = SchoolFee.objects.all()

    def get_serializer_class(self):
        try:
            assert self.request.method is not None
            if self.action in ("list", "retrieve"):
                return ReadSchoolFeeSerializer
            return WriteSchoolFeeSerializer
        except AssertionError as request_method_error:
            raise exceptions.APIException(
                detail="Request Method not Found"
            ) from request_method_error


class SchoolFeesPaymentViewSet(PerformCreateWithAdmin, viewsets.ModelViewSet):
    """
    The School Fees Payment ModelViewSet with all CRUD actions.
    We prefer to use uuid field for lookup
    """

    queryset = SchoolFeesPayment.objects.all().order_by("-updated_at")
    pagination_class = ListPagination
    lookup_field = "uuid"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student__uuid", "school_fee_id"]

    def paginate_queryset(self, queryset):
        if "all" in self.request.query_params:  # type: ignore
            return None
        return super().paginate_queryset(queryset)

    def get_serializer_class(self):
        try:
            assert self.request.method is not None
            if self.action in ("list", "retrieve"):
                return ReadSchoolFeesPaymentSerializer
            return WriteSchoolFeesPaymentSerializer
        except AssertionError as request_method_error:
            raise exceptions.APIException(
                detail="Request Method not Found"
            ) from request_method_error
