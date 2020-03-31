from django.forms import ModelForm, forms
from django import forms

from .models import Assignment, ResultFileUpload, User, Grade, Student


class AssignmentCreateForm(ModelForm):

    class Meta:
        model = Assignment
        exclude = ('created', 'uploder',)


class DocUploadForm(ModelForm):
    class Meta:
        model = ResultFileUpload
        fields = ['exam_name', 'file']


class ResetPassword(forms.Form):

    full_name = forms.CharField(label='Student full name or class name', help_text='Full name example: Juma Rashid Songo, class name example :std1nof2020')