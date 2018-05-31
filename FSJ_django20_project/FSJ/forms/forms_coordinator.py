"""Contains all the Django ModelForms based on the Coordinator model."""

from ..models import Coordinator
from .forms_modelform import ModelForm

class CoordinatorForm(ModelForm):
    """Unrestricted coordinator form, added here for completeness but never used"""
    class Meta:
        model = Coordinator
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref')
        
    def __init__(self, *args, **kwargs):
        super(CoordinatorForm, self).__init__(*args, **kwargs)               
        
    
class CoordinatorRestrictedForm(ModelForm):
    """Restricted coordinaotr form for when a coordinator needs to edit their own profile"""
    class Meta:
        model = Coordinator
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref')
        
    def __init__(self, *args, **kwargs):
        super(CoordinatorRestrictedForm, self).__init__(*args, **kwargs)
        self.fields['ccid'].disabled=True
        self.fields['email'].disabled=True