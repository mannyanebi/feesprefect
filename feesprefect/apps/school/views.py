# Create your views here.
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from feesprefect.apps.school.models import SchoolFeesPayment, Student
from feesprefect.apps.school.serializers import (
    StudentSchoolFeesPaymentSerializer,
    UpdateStudentActiveFieldSerializer,
)
from feesprefect.apps.school.services import sort_and_group_payments_by_school_fees


class SchoolFeesPaymentsAPI(APIView):
    """
    Custom endpoints for school fees payments
    """

    @swagger_auto_schema(
        operation_description="Get a student's school fees payments for an academic class",
        responses={
            status.HTTP_200_OK: "Success",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
        tags=["student-school-fees-payments"],
    )
    # def validate_query_params(self, request):
    #     if request.method == "GET":
    #         query_param_errors = []
    #         for query_param in ["student_uuid", "academic_class_id"]:
    #             if query_param not in request.query_params:
    #                 query_param_errors.append(f"{query_param} is required")
    #         return Response(
    #             {"message": " ,".join(query_param_errors)},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    def get(
        self, request, student_uuid, academic_class_id, format=None
    ):  # pylint: disable=unused-argument, redefined-builtin
        """
        Get a student's school fees payments for an academic class
        """
        # self.validate_query_params(request)
        # student_uuid = request.query_params.get("student_uuid", None)
        # academic_class_id = request.query_params.get("academic_class_id", None)

        student_school_fees_payments = SchoolFeesPayment.objects.filter(
            student__uuid=student_uuid, school_fee__academic_class_id=academic_class_id
        ).order_by("-payment_date")
        sorted_and_grouped_school_fees = sort_and_group_payments_by_school_fees(
            student_school_fees_payments
        )
        serializer = StudentSchoolFeesPaymentSerializer(
            sorted_and_grouped_school_fees, many=True
        )

        return Response(
            {"message": "Success", "errors": None, "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class AdminStudentsAPI(APIView):  # type: ignore
    """
    Custom endpoints for students
    """

    def get_object(
        self, student_uuid: str
    ):  # pylint: disable=missing-function-docstring, no-self-use
        try:
            return Student.objects.get(uuid=student_uuid)
        except Student.DoesNotExist as student_exc:
            raise Http404 from student_exc

    @swagger_auto_schema(
        description="Update a student information, 'active' field",
        request_body=UpdateStudentActiveFieldSerializer(),
        responses={
            status.HTTP_200_OK: UpdateStudentActiveFieldSerializer(),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
        tags=["admin-student-actions"],
        operation_description="Update a student information, 'active' field",
    )
    def post(
        self, request, format=None
    ):  # pylint: disable=unused-argument, redefined-builtin
        """
        Update a student information, 'active' field
        """
        serializer = UpdateStudentActiveFieldSerializer(data=request.data)
        if serializer.is_valid():
            student_uuid = serializer.validated_data["uuid"]  # pyright: ignore
            student = self.get_object(student_uuid)
            student.active = serializer.validated_data["active"]  # pyright: ignore
            student.save()
            return Response(
                {"message": "Success", "errors": None, "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Bad Request", "errors": serializer.errors, "data": None},
            status=status.HTTP_400_BAD_REQUEST,
        )
