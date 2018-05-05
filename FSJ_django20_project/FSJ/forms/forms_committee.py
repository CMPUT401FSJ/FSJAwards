from ..models import Committee
from django.forms import ModelForm, CheckboxSelectMultiple

#Modelform for a committee, this restricts what fields will be enabled/disabled as well as widgets, etc
class CommitteeForm(ModelForm):

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