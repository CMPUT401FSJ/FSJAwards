from ..models import Student
from .forms_modelform import ModelForm
from django.forms import TextInput

# These are the unrestricted and restricted ModelForms used for Students, accessible by Coordinators and Students respectively.
class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'middle_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'student_id', 'gpa')
        
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)               


class StudentEditForm(StudentForm):

    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        self.fields['student_id'].disabled=True


    
class StudentRestrictedForm(ModelForm):

    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'middle_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'student_id', 'gpa')
        widgets = {
            "student_id": TextInput
        }
        
    def __init__(self, *args, **kwargs):
        super(StudentRestrictedForm, self).__init__(*args, **kwargs)
        self.fields['ccid'].disabled=True
        self.fields['email'].disabled=True
        self.fields['year'].disabled=True
        self.fields['student_id'].disabled=True
        self.fields['gpa'].disabled=True
        self.fields['first_name'].disabled=True
        self.fields['middle_name'].disabled=True
        self.fields['last_name'].disabled=True
        
class StudentReadOnlyForm(StudentForm):
    
    def __init__(self, *args, **kwargs):
        super(StudentReadOnlyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True
            