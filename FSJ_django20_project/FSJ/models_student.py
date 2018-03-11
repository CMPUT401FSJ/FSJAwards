from django.db import models
from .models_FSJUser import FSJUser
from django.utils.translation import gettext_lazy as _
from django import forms
from .models_yearofstudy import *

# This class inherits from a standard FSJ User and extends for Student specific attributes and methods
class Student(FSJUser):
    
    program = models.CharField(max_length = 255, verbose_name = _("Program"))
    year = models.ForeignKey(YearOfStudy, on_delete=models.PROTECT)

    def user_class(self):
        return "Student"
            
    def get_program(self):
        return self.program
    
    def student_id(self):
        return self.userid