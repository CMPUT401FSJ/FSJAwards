
from ..models import Award
from django.forms import CheckboxSelectMultiple, DateInput
from .forms_modelform import ModelForm

class DateInput(DateInput):
    input_type = 'date'

#Modelform for an award, this restricts what fields will be enabled/disabled as well as widgets, etc
class AwardForm(ModelForm):

    class Meta:
        model = Award
        exclude = ()
        fields = ('award_name', 'description', 'value', 'programs', 'years_of_study', 'start_date','end_date', 'documents_needed', 'is_active')
        widgets = {
            'programs': CheckboxSelectMultiple,
            'years_of_study': CheckboxSelectMultiple,
            'start_date': DateInput(format = '%Y-%m-%d'),
            'end_date': DateInput(format = '%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super(AwardForm, self).__init__(*args, **kwargs)
        
        
        