"""Contains all Django ModelForms based on the Application Model"""

from ..models import Application
from .forms_modelform import ModelForm

class ApplicationForm(ModelForm):
    """Unrestricted Application form with all fields included"""
    class Meta:
        model = Application
        fields = ('award', 'student', 'is_submitted', 'application_file')
        
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)   
        
        
class ApplicationRestrictedForm(ModelForm):
    """Restricted Application form which students use for applying"""
    class Meta:
        model = Application
        fields = ('application_file',)
            
    def __init__(self, *args, **kwargs):
        super(ApplicationRestrictedForm, self).__init__(*args, **kwargs)
