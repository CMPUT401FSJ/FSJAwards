from .models import Program
from .forms_modelform import ModelForm

#Modelform for a program, this restricts what fields will be enabled/disabled as well as widgets, etc
class ProgramForm(ModelForm):

    class Meta:
        model = Program
        exclude = ()
        fields = ('code', 'name',)