from django.db import models
from .models_FSJUser import FSJUser
from django.utils.translation import gettext_lazy as _
from django.forms import *

# This class inherits from a standard FSJ User and extends for Adjudicator specific attributes and methods
class Adjudicator(FSJUser):
    def user_class(self):
        return "Adjudicator"