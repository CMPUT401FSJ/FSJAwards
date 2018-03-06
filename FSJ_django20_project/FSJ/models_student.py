from django.db import models
from .models_FSJUser import FSJUser
from django.utils.translation import gettext_lazy as _
from django import forms

# This class inherits from a standard FSJ User and extends for Student specific attributes and methods
class Student(FSJUser):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    YEAR_CHOICES = (
        (FIRST, _('First')),
        (SECOND, _('Second')),
        (THIRD, _('Third')),
        (FOURTH, _('Fourth')),
        (FIFTH, _('Fifth')),
    )
    
    program = models.CharField(max_length = 255, verbose_name = _("Program"))
    year = models.IntegerField(blank = False, choices = YEAR_CHOICES, default = FIRST, verbose_name = _("Year of Study"))

    def user_class(self):
        return "Student"
            
    def get_program(self):
        return self.program
    
    def student_id(self):
        return self.userid