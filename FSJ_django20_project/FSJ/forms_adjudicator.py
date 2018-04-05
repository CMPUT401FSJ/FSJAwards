from .models import Adjudicator
from .forms_modelform import ModelForm

class AdjudicatorForm(ModelForm):

    class Meta:
        model = Adjudicator
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref')
        
    def __init__(self, *args, **kwargs):
        super(AdjudicatorForm, self).__init__(*args, **kwargs)               
        
    
class AdjudicatorRestrictedForm(ModelForm):

    class Meta:
        model = Adjudicator
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref')
        
    def __init__(self, *args, **kwargs):
        super(AdjudicatorRestrictedForm, self).__init__(*args, **kwargs)
        self.fields['ccid'].disabled=True
        self.fields['email'].disabled=True