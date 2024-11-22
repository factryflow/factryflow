from ninja import ModelSchema

from common.models import CustomField


# ------------------------------------------------------------------------------
# CustomField Schemas
# ------------------------------------------------------------------------------


class CustomFieldIn(ModelSchema):
    # Schema for CustomField input
    class Meta:
        model = CustomField
        fields = [
            "content_type",
            "name",
            "label",
            "description",
            "field_type",
            "is_required",
        ]


class CustomFieldOut(ModelSchema):
    # Schema for CustomField output
    class Meta:
        model = CustomField
        fields = "__all__"
