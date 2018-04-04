import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models_award import Award
from ..validators import validate_file_extension
from .models_student import Student

class Application(models.Model):
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='applications', verbose_name = _("Award"))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications', verbose_name = _("Student"))
    is_submitted = models.BooleanField(verbose_name = _("Is Submitted"))
    is_reviewed = models.BooleanField(default = False, verbose_name = _("Is Reviewed"))
    application_file = models.FileField(null=True, blank=True, upload_to='documents/', 
                                        verbose_name = _("Application Document"), validators=[validate_file_extension])
    
    def __str__(self):
        return self.student.ccid + "'s application for " + self.award.award_name    
    
    def getawardname(self):
        return self.award.award_name
    
    def getstudentccid(self):
        return self.student.ccid

    def get_status(self):
        if self.is_reviewed:
            return _("Review Completed")
        else:
            return _("Review Pending")

