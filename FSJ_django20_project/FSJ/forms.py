from django.forms import *
from django.utils.translation import gettext_lazy as _
from .models_FSJUser import FSJUser
# Split the forms into packages to allow easier maintenance and multi-user modifications with less conflicts
# Import the forms all into the standard forms.py page so all forms can exist in one place
from .forms_student import *
from .forms_adjudicator import *
from .forms_coordinator import *
from .forms_award import *
from .forms_yearofstudy import *
from .forms_signup import *