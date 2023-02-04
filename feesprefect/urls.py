"""feesprefect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

SchemaView = get_schema_view(
    openapi.Info(
        title="Feesprefect API",
        default_version="1.0.0",
        description="The API for the Feesprefect Admin React App",
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/swagger/",
        SchemaView.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "docs/redoc/",
        SchemaView.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/v1/", include("feesprefect.apps.school.urls", namespace="school")),
]
