from .models_award import Award
from django.forms import ModelForm, CheckboxSelectMultiple, TextInput, Textarea, Select

#Modelform for an award, this restricts what fields will be enabled/disabled as well as widgets, etc
class AwardForm(ModelForm):

    class Meta:
        model = Award
        exclude = ()
        fields = ('award_name', 'description', 'value', 'programs', 'years_of_study', 'deadline', 'documents_needed', 'is_active')
        widgets = {
            'programs': CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(AwardForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            field = self.fields[f]
            widget = field.widget
            if isinstance(widget, TextInput) or isinstance(widget, Textarea) or isinstance(widget, Select):
                field_class = widget.attrs.get('class', '')
                field_class = field_class + ' form-control'
                field.widget.attrs['class'] = field_class