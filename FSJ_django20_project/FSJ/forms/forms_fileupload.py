from django import forms
from django.utils.translation import gettext_lazy as _

class FileUploadForm(forms.Form):
    student_file = forms.FileField(required = False, 
                                   help_text = _("Upload a CSV with fields CCID, ID, First Name, Middle Name, Last Name, Email (Univ), Prog & Year"), 
                                   label = _("Student File"))
    gpa_file = forms.FileField(required = False, help_text = _("Upload a CSV with fields CCID & GPA"), label = _("GPA File"))
    
    
    
    
    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs) 
        for f in self.fields:
            field = self.fields[f]
            widget = field.widget
            field_class = widget.attrs.get('class', '')
            field_class = field_class + ' form-control-file'
            field.widget.attrs['class'] = field_class         