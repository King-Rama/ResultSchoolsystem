from django.forms import ModelForm, forms

from .models import Assignment, ResultFileUpload


class AssignmentCreateForm(ModelForm):

    class Meta:
        model = Assignment
        exclude = ('created', 'uploder',)


class DocUploadForm(ModelForm):
    class Meta:
        model = ResultFileUpload
        fields = ['exam_name', 'file']
