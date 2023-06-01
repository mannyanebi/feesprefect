# Create your views here.
from django.db.models import Sum
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from feesprefect.apps.school.models import AcademicClass, SchoolFeesPayment, Student
from feesprefect.apps.school.serializers import (
    PromoteStudentsInAcademicClassSerializer,
    SchoolStatisticsSerializer,
    StudentSchoolFeesPaymentsByAcademicClassSerializer,
    UpdateStudentActiveFieldSerializer,
)
from feesprefect.apps.school.services import sort_and_group_payments_by_school_fees


class AdminSchoolFeesPaymentsAPI(APIView):
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
        self, request, student_uuid, format=None
    ):  # pylint: disable=unused-argument, redefined-builtin
        """
        Get a student's school fees payments for an academic class
        """
        # self.validate_query_params(request)
        # student_uuid = request.query_params.get("student_uuid", None)
        # academic_class_id = request.query_params.get("academic_class_id", None)

        student_school_fees_payments = SchoolFeesPayment.objects.filter(
            student__uuid=student_uuid
        ).order_by("-payment_date")
        sorted_and_grouped_school_fees = sort_and_group_payments_by_school_fees(
            student_school_fees_payments
        )
        serializer = StudentSchoolFeesPaymentsByAcademicClassSerializer(
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


class AdminAcademicClassesAPI(APIView):  # type: ignore
    """
    Custom endpoints for academic classes
    """

    @swagger_auto_schema(
        description="Promote students in an academic class to a new academic class",
        request_body=PromoteStudentsInAcademicClassSerializer(),
        responses={
            status.HTTP_200_OK: "None",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
        tags=["admin-academic-class-actions"],
        operation_description="Promote students in an academic class to a new academic class",
    )
    def post(
        self, request, format=None
    ):  # pylint: disable=unused-argument, redefined-builtin
        """
        Update a student information, 'active' field
        """
        serializer = PromoteStudentsInAcademicClassSerializer(data=request.data)
        if serializer.is_valid():
            previous_academic_class_id = serializer.validated_data[
                "previous_academic_class_id"
            ]  # pyright: ignore
            new_academic_class_id = serializer.validated_data[
                "new_academic_class_id"
            ]  # pyright: ignore
            students_in_previous_academic_class = Student.objects.filter(
                academic_class_id=previous_academic_class_id, active=True
            )

            students_in_previous_academic_class.update(
                academic_class_id=new_academic_class_id
            )
            return Response(
                {"message": "Success", "errors": None, "data": None},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Bad Request", "errors": serializer.errors, "data": None},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AdminSchoolStatisticsAPI(APIView):
    """
    Custom endpoints for school fees payments
    """

    @swagger_auto_schema(
        operation_description="Gets statistics of students, classes and school fees payments",
        responses={
            status.HTTP_200_OK: "Success",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
        tags=["school-statistics"],
    )
    def get(
        self, request, format=None
    ):  # pylint: disable=unused-argument, redefined-builtin
        """
        Gets statistics of students, classes and school fees payments
        """

        students_count = Student.objects.filter(active=True).count()
        academic_classes_count = AcademicClass.objects.all().count()
        total_school_fees_payments: dict = SchoolFeesPayment.objects.aggregate(
            Sum("amount_paid")
        )

        serializer = SchoolStatisticsSerializer(
            {
                "students_count": students_count,
                "academic_classes_count": academic_classes_count,
                "school_fees_payments_count": total_school_fees_payments[
                    "amount_paid__sum"
                ],
            }
        )

        return Response(
            {"message": "Success", "errors": None, "data": serializer.data},
            status=status.HTTP_200_OK,
        )
