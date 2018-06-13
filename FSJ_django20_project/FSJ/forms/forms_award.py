"""Contains all Django ModelForms relating to the Award Model and related custom fields"""

from ..models import Award
from django.forms import CheckboxSelectMultiple, DateInput
from django import forms
from .forms_modelform import ModelForm
from django.utils.translation import gettext_lazy as _
from datetime import datetime



class DateInput(DateInput):
    """A DateInput form which uses 'date' as the input type rather than the text default"""
    input_type = 'date'
    template_name = 'FSJ/date_field.html'

#Modelform for an award, this restricts what fields will be enabled/disabled as well as widgets, etc
class AwardForm(ModelForm):
    """Unrestricted Award form with all fields enabled except the review comment"""
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
        """Validates award dates by checking that the start date is before the end date"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
    
        if start_date and end_date:
            if start_date > end_date:
                msg = forms.ValidationError(_("The start date must be later than the end date."))
                self.add_error('start_date', msg)

    def clean_end_date(self):
        data = self.cleaned_data['end_date']
        end_date = data.replace(hour=23, minute=59, second=59)
        return end_date


class AwardReviewCommentForm(ModelForm):
    """Restricted Award form used in the coordinator's final review of an award"""
    class Meta:
        model = Award
        fields = ('review_comment',)
