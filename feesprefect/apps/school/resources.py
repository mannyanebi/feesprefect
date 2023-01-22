from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from feesprefect.apps.accounts.models import FeesprefectAdmin

from .models import AcademicClass, Student


class StudentResource(resources.ModelResource):
    academic_class = fields.Field(
        attribute="academic_class",
        column_name="academic_class",
        widget=ForeignKeyWidget(AcademicClass, "id"),
    )

    created_by = fields.Field(
        attribute="created_by",
        column_name="created_by",
        widget=ForeignKeyWidget(FeesprefectAdmin, "id"),
    )

    class Meta:
        model = Student
        import_id_fields = ("id",)
        fields = ("id", "name", "academic_class", "created_by")
        force_init_instance = True
        use_bulk = True
