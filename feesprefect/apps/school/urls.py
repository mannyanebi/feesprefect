from django.urls import include, path
from rest_framework.routers import DefaultRouter

from feesprefect.apps.school.viewsets import StudentViewSet

app_name = "school"

router = DefaultRouter()
router.register(r"students", StudentViewSet)

urlpatterns = [path("", include(router.urls))]
