from django.urls import path

from .views import HomepageRedirectView

app_name = "core"

urlpatterns = [
    path("", HomepageRedirectView.as_view(), name="homepage-redirect"),
]
