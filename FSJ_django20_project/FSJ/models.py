from django.db import models

# Split the models into packages to allow easier maintenance and multi-user modifications with less conflicts
# Import the models all into the standard models.py page so all models can exist in one place
from .models_student import Student
from .models_adjudicator import Adjudicator
from .models_coordinator import Coordinator
from .models_award import Award
from .models_yearofstudy import YearOfStudy
from .models_committee import Committee
from .models_program import Program
from .models_yearofstudy import YearOfStudy
from .models_application import Application
