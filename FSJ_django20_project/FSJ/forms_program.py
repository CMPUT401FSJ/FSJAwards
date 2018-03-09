from .models_program import Program
from django.forms import ModelForm, CheckboxSelectMultiple

#Modelform for a program, this restricts what fields will be enabled/disabled as well as widgets, etc
class ProgramForm(ModelForm):

    class Meta:
        model = Program
        exclude = ()
        fields = ('name',)