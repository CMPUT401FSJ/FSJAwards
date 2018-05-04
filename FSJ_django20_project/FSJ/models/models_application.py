import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models_award import Award
from ..validators import validate_file_extension
from .models_student import Student
from .models_adjudicator import Adjudicator
from .models_FSJUser import FSJUser

class Application(models.Model):
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='applications', verbose_name = _("Award"))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications', verbose_name = _("Student"))
    is_submitted = models.BooleanField(verbose_name = _("Is Submitted"))
    is_reviewed = models.BooleanField(default = False, verbose_name = _("Is Reviewed"))
    is_archived = models.BooleanField(default = False, verbose_name = _("Is Archived"))
    application_file = models.FileField(null=True, blank=True, upload_to='documents/', 
                                        verbose_name = _("Application Document"), validators=[validate_file_extension])
    viewed = models.ManyToManyField(FSJUser, related_name='viewed', verbose_name = _("Viewed"))
    adjudicators = models.ManyToManyField(Adjudicator, related_name='applications', verbose_name = _("Adjudicators"))
    
    def __str__(self):
        return self.student.ccid + "'s application for " + self.award.award_name    
    
    def getawardname(self):
        return self.award.award_name
    
    def getstudentccid(self):
        return self.student.ccid

        
    def get_status(self, FSJ_user):
        
        if FSJ_user.user_class() == "Coordinator":
            
            if self.is_reviewed:
                return _("Review Completed")                
            elif self.viewed.filter(pk = FSJ_user.pk):
                return _("Review Pending")   
            else:
                return _("View Application")
            
        elif FSJ_user.user_class() == "Adjudicator":
            
            if FSJ_user in self.adjudicators.all():
                return _("Review Completed")
            elif self.viewed.filter(pk = FSJ_user.pk):
                return _("Review Pending")
            else:
                return _("View Application")
    

    def add_viewed(self, FSJ_user):
        if FSJ_user not in self.viewed.all():
            self.viewed.add(FSJ_user)
            
            
    def add_reviewed(self, FSJ_user):
        if FSJ_user not in self.adjudicators.all():
            self.adjudicators.add(FSJ_user)            
            
    def delete_viewed(self, FSJ_user):
        try:
            self.viewed.filter(pk = FSJ_user.pk).delete()
            
        except:
            pass
        
        
    def delete_reviewed(self, FSJ_user):
        try:
            self.adjudicators.filter(pk = FSJ_user.pk).delete()
            
        except:
            pass        