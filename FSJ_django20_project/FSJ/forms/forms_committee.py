"""Contains all Django ModelForms based on the Committee model"""

from ..models import Committee, Adjudicator
from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple

class CommitteeForm(ModelForm):
    """Unrestricted Committee form. Choices for awards are restricted based on those which are not already associated
    with an award.

    available_awards -- a list of the awards currently not associated with a committee
    """

    adjudicators = forms.ModelMultipleChoiceField(queryset=Adjudicator.objects.order_by('ccid'), widget=CheckboxSelectMultiple)

    class Meta:
        model = Committee
        exclude = ()
        fields = ('committee_name', 'adjudicators', 'awards')
        widgets = {
            'adjudicators': CheckboxSelectMultiple, 
            'awards': CheckboxSelectMultiple
        }

    def __init__(self, available_awards, *args, **kwargs):
        super(CommitteeForm, self).__init__(*args, **kwargs)
        self.fields['awards'].widget.instance = self.instance
        self.fields['awards'].choices = available_awards