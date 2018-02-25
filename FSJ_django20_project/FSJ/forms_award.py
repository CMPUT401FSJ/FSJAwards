from .models_award import Award
from django.forms import ModelForm, CheckboxSelectMultiple

class AwardForm(ModelForm):

    class Meta:
        model = Award
        exclude = ()
        #uncomment this out when awards are ready for multiple years of study
        # fields = ('award_name', 'description', 'value', 'programs', 'years_of_study', 'deadline', 'documents_needed', 'is_active')
        # widgets = {
        #     'years_of_study': CheckboxSelectMultiple(),
        # }

    def __init__(self, *args, **kwargs):
        super(AwardForm, self).__init__(*args, **kwargs)
        
        
    
class AwardRestrictedForm(ModelForm):

    class Meta:
        model = Award
        fields = ('award_name', 'description', 'value', 'programs', 'years_of_study', 'deadline', 'documents_needed', 'is_active')
        widgets = {
            'years_of_study': CheckboxSelectMultiple(),
        }
        
    def __init__(self, *args, **kwargs):
        super(AwardRestrictedForm, self).__init__(*args, **kwargs)
        #self.fields['awardid'].disabled=True