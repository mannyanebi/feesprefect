from django.urls import path
from rest_framework.authtoken import views

from .views import AdminLogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", views.obtain_auth_token, name="login-obtain-json-token"),
    path("logout/", AdminLogoutView.as_view(), name="logout"),
]
