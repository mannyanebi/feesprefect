# Create your views here.
from django.views.generic.base import RedirectView


class HomepageRedirectView(RedirectView):
    url = "/admin"
