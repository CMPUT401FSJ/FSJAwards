import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models_award import Award
from .models_student import Student

class ArchivedApplication(models.Model):
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='archived_applications', verbose_name = _("Award"))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='archived_applications', verbose_name = _("Student"))
    application_file = models.FileField(null=True, blank=True, upload_to='documents/', verbose_name = _("Application Document"))
    
    def __str__(self):
        return self.student.ccid + "'s application for " + self.award.award_name    
    
    def getawardname(self):
        return self.award.award_name
    
    def getstudentccid(self):
        return self.student.ccid