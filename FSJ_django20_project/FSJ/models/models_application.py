import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models_award import Award
from ..validators import validate_file_extension
from django.core.validators import FileExtensionValidator
from .models_student import Student
from .models_adjudicator import Adjudicator
from .models_FSJUser import FSJUser
import os
from django.dispatch import receiver


class Application(models.Model):
    """Represents a student's application for a specific award, which is then reviewed by adjudicators and the
    coordinator.

    application_id -- unique auto-generated ID
    award -- foreign key relating the application to its associated award
    student -- foreign key relating the application to the student who submitted it
    is_submitted -- boolean representing whether the application has been submitted for review or not
    is_reviewed -- boolean representing whether the application has been reviewed by the coordinator or not
    is_archived -- bolean representing whether the application has been archived by the coordinator or not
    application_file -- a file which may or may not be attached to the application depending on whether the award
    calls for a required document
    viewed -- a list of all the adjudicators/coordinators that have viewed the application
    adjudicators -- a list of all the adjudicators who have reviewed the application
    """
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='applications', verbose_name = _("Award"))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications', verbose_name = _("Student"))
    is_submitted = models.BooleanField(verbose_name = _("Is Submitted"))
    is_reviewed = models.BooleanField(default = False, verbose_name = _("Is Reviewed"))
    is_archived = models.BooleanField(default = False, verbose_name = _("Is Archived"))
    is_eligible = models.BooleanField(default = True, verbose_name = _("Is Eligible"))
    application_file = models.FileField(null=True, blank=True, upload_to='documents/', 
                                        verbose_name = _("Application Document"), validators=[FileExtensionValidator(["pdf"])])
    viewed = models.ManyToManyField(FSJUser, related_name='viewed', verbose_name = _("Viewed"))
    adjudicators = models.ManyToManyField(Adjudicator, related_name='applications', verbose_name = _("Adjudicators"))
    
    def __str__(self):
        return self.student.ccid + "'s application for " + self.award.name
    
    def getawardname(self):
        return self.award.name
    
    def getstudentccid(self):
        return self.student.ccid

        
    def get_status(self, FSJ_user):
        """Returns the review status of the application with regards to a specific user

        FSJ_user -- the user who is checking if they've reviewed the application"""

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
        """Adds a user to the list of those who have viewed the application

        FSJ_user -- the user to be added to the list
        """
        if FSJ_user not in self.viewed.all():
            self.viewed.add(FSJ_user)
            
            
    def add_reviewed(self, FSJ_user):
        """Adds an adjudicator to the list of adjudicators who have reviewed the application.

        FSJ_user -- the user to be added to the list
        """
        if FSJ_user not in self.adjudicators.all():
            self.adjudicators.add(FSJ_user)            
            
    def delete_viewed(self, FSJ_user):
        """Removes a user from the list of users who have viewed the application

        FSJ_user -- the user to be removed
        """
        try:
            self.viewed.remove(FSJ_user)
            
        except:
            pass
        
        
    def delete_reviewed(self, FSJ_user):
        """Removes a user from the list of adjudicators who have reviewed the application"""
        try:
            self.adjudicators.remove(FSJ_user)
            
        except:
            pass        
        
        
    def is_adj_reviewed(self, FSJ_user):
        """Checks if a specific adjudicator has reviewed this application

        FSJ_user -- the user to be checked against the list of adjudicators
        """
        
        if FSJ_user in self.adjudicators.all():
            return True
        
        else:
            return False

# Code adapted from from https://stackoverflow.com/questions/16041232/django-delete-filefield/16041527
@receiver(models.signals.post_delete, sender=Application)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.application_file:
        if os.path.isfile(instance.application_file.path):
            os.remove(instance.application_file.path)

@receiver(models.signals.pre_save, sender=Application)
def auto_delete_file_on_change(sender, instance, **kwargs):

    if not instance.pk:
        return False

    try:
        old_file = Application.objects.get(pk=instance.pk).application_file
    except:
        return False

    if old_file:
        new_file = instance.application_file
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)