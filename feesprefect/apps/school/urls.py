from django.urls import include, path
from rest_framework.routers import DefaultRouter

from feesprefect.apps.school.viewsets import AcademicClassViewSet, StudentViewSet

app_name = "school"

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="student")
router.register(r"academic-class", AcademicClassViewSet, basename="academic-class")

urlpatterns = [path("", include(router.urls))]
