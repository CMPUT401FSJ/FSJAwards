"""All ModelForms based on the Student model"""

from ..models import Student
from .forms_modelform import ModelForm
from django.forms import TextInput

class StudentForm(ModelForm):
    """Unrestricted student form available to coordinators creating a new student"""
    class Meta:
        model = Student
        fields = ('ccid', 'first_name', 'middle_name', 'last_name', 'email', 'lang_pref', 'program', 'year', 'student_id', 'gpa')
        
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)               


class StudentEditForm(StudentForm):
    """Semi-restricted form available to coordinators who are editing students"""
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        self.fields['student_id'].disabled=True


    
class StudentRestrictedForm(ModelForm):
    """Restricted form available to students who are editing their own profiles"""
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
    """Read-only form available to coordinators and adjudicators who are viewing students"""
    def __init__(self, *args, **kwargs):
        super(StudentReadOnlyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True
            