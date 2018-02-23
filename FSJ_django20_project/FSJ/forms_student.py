from .models_student import Student
from django.forms import ModelForm

class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'userid')
        
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)               
        
    
class StudentRestrictedForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'program', 'year')
        
    def __init__(self, *args, **kwargs):
        super(StudentRestrictedForm, self).__init__(*args, **kwargs)
        self.fields['ccid'].disabled=True
        self.fields['email'].disabled=True
        self.fields['year'].disabled=True
        