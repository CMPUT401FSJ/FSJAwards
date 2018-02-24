from .models_adjudicator import Adjudicator
from django.forms import ModelForm

class AdjudicatorForm(ModelForm):

    class Meta:
        model = Adjudicator
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'userid')
        
    def __init__(self, *args, **kwargs):
        super(AdjudicatorForm, self).__init__(*args, **kwargs)               
        
    
class AdjudicatorRestrictedForm(ModelForm):

    class Meta:
        model = Adjudicator
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'userid')
        
    def __init__(self, *args, **kwargs):
        super(AdjudicatorRestrictedForm, self).__init__(*args, **kwargs)
        self.fields['ccid'].disabled=True
        self.fields['email'].disabled=True

