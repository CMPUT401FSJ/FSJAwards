from django.db import models

# Split the models into packages to allow easier maintenance and multi-user modifications with less conflicts
# Import the models all into the standard models.py page so all models can exist in one place
from .models.models_student import Student
from .models.models_adjudicator import Adjudicator
from .models.models_coordinator import Coordinator
from .models.models_award import Award
from .models.models_committee import Committee
from .models.models_program import Program
from .models.models_yearofstudy import YearOfStudy
from .models.models_application import Application
from .models.models_committee import Committee
from .models.models_FSJUser import FSJUser
from .models.models_comment import Comment