from ..models import YearOfStudy
from django.forms import CheckboxSelectMultiple
from .forms_modelform import ModelForm

#Modelform for an award, this restricts what fields will be enabled/disabled as well as widgets, etc
class YearOfStudyForm(ModelForm):

    class Meta:
        model = YearOfStudy
        exclude = ()
        fields = ('year',)

    def __init__(self, *args, **kwargs):

        super(YearOfStudyForm, self).__init__(*args, **kwargs)