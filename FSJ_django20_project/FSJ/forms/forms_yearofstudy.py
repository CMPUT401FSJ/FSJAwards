from ..models import YearOfStudy
from django.forms import CheckboxSelectMultiple
from .forms_modelform import ModelForm

class YearOfStudyForm(ModelForm):
    """Unrestricted form for the Year Of Study model which coordinators use to create a new year"""
    class Meta:
        model = YearOfStudy
        exclude = ()
        fields = ('year',)

    def __init__(self, *args, **kwargs):

        super(YearOfStudyForm, self).__init__(*args, **kwargs)