from rest_framework import renderers

from feesprefect.apps.core.utils.parsers import SnakeCaseParser
from feesprefect.apps.core.utils.renderers import (
    BrowsableCamelCaseRenderer,
    CamelCaseRenderer,
)


class ToCamelCase(renderers.BrowsableAPIRenderer):
    renderer_classes = (
        BrowsableCamelCaseRenderer,
        CamelCaseRenderer,
    )


class FromCamelCase:
    parser_classes = (SnakeCaseParser,)


# Reference
# https://www.hacksoft.io/blog/how-to-deal-with-cases-mismatch-between-django-and-react


# HttpRequestType = NewType('HttpRequestType', HttpRequest)

# class RequestType(TypedDict):
#     request: HttpRequestType

# class RequestUserType(TypedDict):
#     self: RequestType
class PerformCreateWithAdmin:
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user  # pylint: disable=no-member # type: ignore
        )
