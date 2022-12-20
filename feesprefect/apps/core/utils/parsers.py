# pylint: skip-file
from rest_framework import parsers

from .transformers import deep_snake_case_transform


class SnakeCaseParser(parsers.JSONParser):
    def parse(self, stream, *args, **kwargs):
        data = super().parse(stream, *args, **kwargs)

        return deep_snake_case_transform(data)


# Reference
# https://www.hacksoft.io/blog/how-to-deal-with-cases-mismatch-between-django-and-react
