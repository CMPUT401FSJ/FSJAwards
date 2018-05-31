from django.db import models
from .models_FSJUser import FSJUser
from django.utils.translation import gettext_lazy as _
from django.forms import *

class Adjudicator(FSJUser):
    """A subclass of FSJUser for the user role which evaluates and ranks applications"""
    def user_class(self):
        return "Adjudicator"