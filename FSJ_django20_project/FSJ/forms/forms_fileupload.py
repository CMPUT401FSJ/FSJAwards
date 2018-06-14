"""Contains FileUploadForm class"""

from django import forms
from django.utils.translation import gettext_lazy as _

class FileUploadForm(forms.Form):
    """Used by the coordinator to upload CSV files containing information about students and their GPAs"""

    CHOICES = [('utf-8-sig', "UTF-8"), ('windows-1252', "Windows")]

    encoding = forms.ChoiceField(required = True, choices = CHOICES, widget = forms.RadioSelect, label = _("CSV Encoding"), help_text = _("Please choose the encoding for your CSV."))
    student_file = forms.FileField(required = False, 
                                   help_text = _("Upload a CSV with fields CCID, ID, First Name, Middle Name, Last Name, Email (Univ), Prog & Year"), 
                                   label = _("Student File"))
    gpa_file = forms.FileField(required = False, help_text = _("Upload a CSV with fields ID, GPA & Credits"), label = _("GPA File"))
    
    
    
    
    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs) 
        for f in self.fields:
            field = self.fields[f]
            widget = field.widget
            field_class = widget.attrs.get('class', '')
            field_class = field_class + ' form-control-file'
            field.widget.attrs['class'] = field_class