
from ..models import Award
from django.forms import CheckboxSelectMultiple, DateInput
from django import forms
from .forms_modelform import ModelForm
from django.utils.translation import gettext_lazy as _


class DateInput(DateInput):
    input_type = 'date'
    template_name = 'FSJ/date_field.html'

#Modelform for an award, this restricts what fields will be enabled/disabled as well as widgets, etc
class AwardForm(ModelForm):

    class Meta:
        model = Award
        exclude = ()
        fields = ('name', 'description', 'value', 'programs', 'years_of_study', 'start_date','end_date', 'documents_needed', 'is_active')
        widgets = {
            'programs': CheckboxSelectMultiple,
            'years_of_study': CheckboxSelectMultiple,
            'start_date': DateInput(format = '%Y-%m-%d'),
            'end_date': DateInput(format = '%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super(AwardForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
    
        if start_date and end_date:
            if start_date > end_date:
                msg = forms.ValidationError(_("The start date must be later than the end date."))
                self.add_error('start_date', msg)


class AwardReviewCommentForm(ModelForm):

    class Meta:
        model = Award
        fields = ('review_comment',)
