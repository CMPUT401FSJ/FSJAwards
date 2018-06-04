from django.db import models
from .models_FSJUser import FSJUser
from django.utils.translation import gettext_lazy as _
from django.forms import *

class Coordinator(FSJUser):
    """A subclass of FSJUser representing the coordinator, who is the person with the most control over the system"""
    def user_class(self):
        return "Coordinator"