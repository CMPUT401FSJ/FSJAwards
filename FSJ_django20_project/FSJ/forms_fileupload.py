from django import forms

class FileUploadForm(forms.Form):
    student_file = forms.FileField(required = False, help_text = ("Upload a CSV with fields CCID, ID, First Name, Last Name, Email (Univ), Prog & Year"))
    gpa_file = forms.FileField(required = False, help_text = ("Upload a CSV with fields CCID & GPA"))