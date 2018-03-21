from django.forms import ModelForm as DjangoModelForm, TextInput, Textarea, Select, EmailInput, NumberInput

class ModelForm(DjangoModelForm):
    
    def __init__(self, *args, **kwargs):
        def _is_form_control_widget(widget):
            if isinstance(widget, TextInput):
                return True
            if isinstance(widget, Textarea):
                return True
            if isinstance(widget, Select):
                return True
            if isinstance(widget, EmailInput):
                return True
            if isinstance(widget, NumberInput):
                return True      
            return False
        
        super(ModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            field = self.fields[f]
            widget = field.widget
            if _is_form_control_widget(widget):
                field_class = widget.attrs.get('class', '')
                field_class = field_class + ' form-control'
                field.widget.attrs['class'] = field_class   