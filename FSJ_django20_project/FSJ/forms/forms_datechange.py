from django import forms
from django.forms import DateInput
from django.utils.translation import gettext_lazy as _

class DateInput(DateInput):
    input_type = 'date'

class DateChangeForm(forms.Form):

    start_date = forms.DateTimeField(required = False, widget = DateInput(format = '%Y-%m-%d'), label = _("Start date"))
    end_date = forms.DateTimeField(required = False, widget = DateInput(format = '%Y-%m-%d'), label = _("End date"))
    
    def __init__(self, *args, **kwargs):
        super(DateChangeForm, self).__init__(*args, **kwargs)    
        
        for f in self.fields:
            field = self.fields[f]
            widget = field.widget
            field_class = widget.attrs.get('class', '')
            field_class = field_class + ' form-control'
            field.widget.attrs['class'] = field_class        