from django import forms
import waffle

from .models import CustomField
from django_select2 import forms as s2forms


# ------------------------------------------------------------------------------
# CustomField FORM
# ------------------------------------------------------------------------------


class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = [
            "name",
            "label",
            "field_type",
            "content_type",
            "description",
            "is_required",
        ]
        labels = {
            "name": "Field Name",
            "label": "Field Label",
            "field_type": "Field Type",
            "content_type": "Content Type",
            "description": "Description",
            "is_required": "Is Required",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "label": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "field_type": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "content_type": forms.Select(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "is_required": forms.CheckboxInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-1/8 p-3"
                }
            ),
        }


# ------------------------------------------------------------------------------
# MultiSelectWidget and SelectWidget for Select Field
# ------------------------------------------------------------------------------

CSS_STYLE_FORM_FIELD = "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3 bg-inherit"


def get_multi_select_widget(model):
    if waffle.switch_is_active("multi_select_widget"):
        return s2forms.ModelSelect2MultipleWidget(
            model=model,
            search_fields=["name__icontains"],
            attrs={
                "data-minimum-input-length": 0,
                "data-placeholder": f"Select {model._meta.verbose_name_plural}",
                "data-close-on-select": "false",
                "class": CSS_STYLE_FORM_FIELD,
            },
        )

    return forms.SelectMultiple(
        attrs={
            "class": CSS_STYLE_FORM_FIELD
        }
    )


def get_select_widget(model):
    if waffle.switch_is_active("multi_select_widget"):
        return s2forms.ModelSelect2Widget(
            model=model,
            search_fields=["name__icontains"],
            attrs={
                "data-minimum-input-length": 0,
                "data-placeholder": f"Select {model._meta.verbose_name_plural}",
                "data-close-on-select": "true",
                "class": CSS_STYLE_FORM_FIELD,
            },
        )

    return forms.Select(
        attrs={
            "class": CSS_STYLE_FORM_FIELD
        }
    )
