from django.db import models
from django.utils.translation import gettext_lazy as _
from .models_award import Award
from .models_student import Student

class Application(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(verbose_name = _("Is Submitted"))
    
    def __str__(self):
        return self.award.award_name    