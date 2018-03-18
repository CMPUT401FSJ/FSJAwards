from django import forms

class FileUploadForm(forms.Form):
    student_file = forms.FileField(required = False)
    gpa_file = forms.FileField(required = False)