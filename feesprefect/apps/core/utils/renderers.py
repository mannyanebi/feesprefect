# pylint: skip-file
from rest_framework import renderers

from .transformers import deep_camel_case_transform


class CamelCaseRenderer(renderers.JSONRenderer):
    def render(self, data, *args, **kwargs):
        camelized_data = deep_camel_case_transform(data)

        return super().render(camelized_data, *args, **kwargs)


class BrowsableCamelCaseRenderer(renderers.BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return CamelCaseRenderer()


# Reference
# https://www.hacksoft.io/blog/how-to-deal-with-cases-mismatch-between-django-and-react
