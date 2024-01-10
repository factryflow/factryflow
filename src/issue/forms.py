from django import forms
from taggit.forms import TagWidget

from .models import Comment, Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description", "thumbnail", "tags"]
        labels = {
            "title": "Title",
            "description": "Description",
            "thumbnail": "Thumbnail",
            "tags": "Tags",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3"
                }
            ),
            "description": forms.TextArea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
            "thumbnail": forms.FileInput(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block p-3",
                }
            ),
            "tags": TagWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {
            "body": "Body",
        }
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "border border-[#E1E3EA] text-gray-900 text-sm rounded-md focus:ring-blue-500 focus-visible:outline-none block w-full p-3",
                }
            ),
        }
