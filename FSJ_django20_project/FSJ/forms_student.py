from .models_student import Student
from .forms import ModelForm, TextInput, Textarea, Select, EmailInput, NumberInput

# These are the unrestricted and restricted ModelForms used for Students, accessible by Coordinators and Students respectively.
class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'userid')
        
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)               
        for f in self.fields:
            field = self.fields[f]
            widget = field.widget
            if isinstance(widget, TextInput) or isinstance(widget, Textarea) or isinstance(widget, Select) or isinstance(widget, EmailInput) or isinstance(widget, NumberInput):
                field_class = widget.attrs.get('class', '')
                field_class = field_class + ' form-control'
                field.widget.attrs['class'] = field_class          
    
class StudentRestrictedForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'userid')
        
    def __init__(self, *args, **kwargs):
        super(StudentRestrictedForm, self).__init__(*args, **kwargs)
        self.fields['ccid'].disabled=True
        self.fields['email'].disabled=True
        self.fields['year'].disabled=True
        for f in self.fields:
            field = self.fields[f]
            widget = field.widget
            if isinstance(widget, TextInput) or isinstance(widget, Textarea) or isinstance(widget, Select) or isinstance(widget, EmailInput) or isinstance(widget, NumberInput):
                field_class = widget.attrs.get('class', '')
                field_class = field_class + ' form-control'
                field.widget.attrs['class'] = field_class        