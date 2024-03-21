from django import forms
from .models import *

# ------------------------------------------------------------------------------
# TaskResource Assignment Forms
# ------------------------------------------------------------------------------

class TaskResourceAssigmentForm(forms.ModelForm):
    class Meta:
        model = TaskResourceAssigment
        fields = "__all__"
        exclude = ["created_by", "updated_by", "created_at", "updated_at"]
        labels = {
            "task": "Task",
            "assigment_rule": "Assigment Rule",
            "resource_pool": "Resource Pool",
            "resource_count": "Resource Count",
            "use_all_resources": "Use All Resources",
        }
        widgets = {
            "task": forms.Select(attrs={"class": "form-control"}),
            "assigment_rule": forms.Select(attrs={"class": "form-control"}),
            "resource_pool": forms.SelectMultiple(attrs={"class": "form-control"}),
            "resource_count": forms.NumberInput(attrs={"class": "form-control"}),
            "use_all_resources": forms.CheckboxInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "task": "Select the task to assign resources to.",
            "assigment_rule": "Select the assigment rule to apply to the task.",
            "resource_pool": "Select the resource pool to assign to the task.",
            "resource_count": "Enter the number of resources to assign to the task.",
            "use_all_resources": "Check this box to assign all resources in the pool to the task.",
        }



# ------------------------------------------------------------------------------
# AssigmentRule Forms
# ------------------------------------------------------------------------------

class AssigmentRuleForm(forms.ModelForm):
    class Meta:
        model = AssigmentRule
        fields = ["external_id", "name", "work_center", "is_active", "notes", "description"]
        exclude = ["created_by", "updated_by", "created_at", "updated_at"]
        labels = {
            "external_id": "External ID",
            "name": "Name",
            "work_center": "Work Center",
            "is_active": "Is Active",
            "notes": "Notes",
            "description": "Description",
        }
        widgets = {
            "external_id": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "work_center": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


# ------------------------------------------------------------------------------
# AssigmentRuleCriteria Forms
# ------------------------------------------------------------------------------

class AssigmentRuleCriteriaForm(forms.ModelForm):
    class Meta:
        model = AssigmentRuleCriteria
        fields = "__all__"
        exclude = ["created_by", "updated_by", "created_at", "updated_at"]
        labels = {
            "assigment_rule": "Assigment Rule",
            "field": "Field",
            "operator": "Operator",
            "value": "Value",
        }
        widgets = {
            "assigment_rule": forms.Select(attrs={"class": "form-control"}),
            "field": forms.TextInput(attrs={"class": "form-control"}),
            "operator": forms.Select(attrs={"class": "form-control"}),
            "value": forms.TextInput(attrs={"class": "form-control"}),
        }

# ------------------------------------------------------------------------------
# AssignmentConstraint Forms
# ------------------------------------------------------------------------------

class AssignmentConstraintForm(forms.ModelForm):
    class Meta:
        model = AssignmentConstraint
        fields = "__all__"
        exclude = ["created_by", "updated_by", "created_at", "updated_at"]
        labels = {
            "task": "Task",
            "assignment_rule": "Assignment Rule",
            "resource_pool": "Resource Pool",
            "resources": "Resources",
            "work_units": "Work Units",
            "required_units": "Required Units",
            "is_active": "Is Active",
            "is_direct": "Is Direct",
        }
        widgets = {
            "task": forms.Select(attrs={"class": "form-control"}),
            "assignment_rule": forms.Select(attrs={"class": "form-control"}),
            "resource_pool": forms.Select(attrs={"class": "form-control"}),
            "resources": forms.SelectMultiple(attrs={"class": "form-control"}),
            "work_units": forms.SelectMultiple(attrs={"class": "form-control"}),
            "required_units": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-control"}),
            "is_direct": forms.CheckboxInput(attrs={"class": "form-control"}),
        }