from .models_student import Student
from .forms_modelform import ModelForm

# These are the unrestricted and restricted ModelForms used for Students, accessible by Coordinators and Students respectively.
class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'ualberta_id')
        
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)               
        
    
class StudentRestrictedForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'ualberta_id')
        
    def __init__(self, *args, **kwargs):
        super(StudentRestrictedForm, self).__init__(*args, **kwargs)
        self.fields['ccid'].disabled=True
        self.fields['email'].disabled=True
        self.fields['year'].disabled=True   
        
class StudentReadOnlyForm(StudentForm):
    
    def __init__(self, *args, **kwargs):
        super(StudentReadOnlyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True
            