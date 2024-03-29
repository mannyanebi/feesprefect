from django.urls import include, path
from rest_framework.routers import DefaultRouter

from feesprefect.apps.school.views import (
    AdminAcademicClassesAPI,
    AdminSchoolFeesPaymentsAPI,
    AdminSchoolStatisticsAPI,
    AdminStudentsAPI,
)
from feesprefect.apps.school.viewsets import (
    AcademicClassViewSet,
    AcademicSessionViewSet,
    SchoolFeesPaymentViewSet,
    SchoolFeesViewSet,
    StudentViewSet,
)

app_name = "school"

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"academic-class", AcademicClassViewSet, basename="academic-class")
router.register(
    r"academic-session", AcademicSessionViewSet, basename="academic-session"
)
router.register(r"school-fees", SchoolFeesViewSet, basename="school-fees")
router.register(
    r"school-fees-payment", SchoolFeesPaymentViewSet, basename="school-fees-payments"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "student-school-fees-payments/<uuid:student_uuid>/",
        AdminSchoolFeesPaymentsAPI.as_view(),  # pyright: ignore
        name="student-school-fees-payments",
    ),
    path(
        "students-admin-actions/",
        AdminStudentsAPI.as_view(),  # pyright: ignore
        name="students-admin-actions",
    ),
    path(
        "academic-class-admin-actions/",
        AdminAcademicClassesAPI.as_view(),  # pyright: ignore
        name="students-admin-actions",
    ),
    path(
        "school-statistics/",
        AdminSchoolStatisticsAPI.as_view(),  # pyright: ignore
        name="school-statistics",
    ),
]
