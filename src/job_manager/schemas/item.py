from ninja import Field, ModelSchema

from job_manager.models import Item

# ------------------------------------------------------------------------------
# Item Schemas
# ------------------------------------------------------------------------------


class ItemIn(ModelSchema):
    class Meta:
        model = Item
        fields = ["name", "external_id", "notes", "description", "custom_fields"]


class ItemOut(ModelSchema):
    class Meta:
        model = Item
        fields = "__all__"
