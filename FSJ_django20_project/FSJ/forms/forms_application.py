from ..models import Application
from .forms_modelform import ModelForm

class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        fields = ('award', 'student', 'is_submitted', 'application_file')
        
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)   
        
        
class ApplicationRestrictedForm(ModelForm):
    
    class Meta:
        model = Application
        fields = ('application_file',)
            
    def __init__(self, *args, **kwargs):
        super(ApplicationRestrictedForm, self).__init__(*args, **kwargs)
