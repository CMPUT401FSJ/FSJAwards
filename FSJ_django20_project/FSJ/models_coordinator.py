from django.db import models
from .models_FSJUser import FSJUser
from django.utils.translation import gettext_lazy as _
from django.forms import *

# This class inherits from a standard FSJ User and extends for Coordinator specific attributes and methods
class Coordinator(FSJUser):
    def user_class(self):
        return "Coordinator"