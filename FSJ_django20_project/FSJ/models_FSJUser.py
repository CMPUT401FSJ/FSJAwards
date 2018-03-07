from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class FSJUser(models.Model):
    # List the languages a user may choose from in human readable format and also make them accessible in other files 
    # via FSJUser.LANG_CHOICES, FSJUser.ENGLISH, etc.
    FRENCH = 'fr'
    ENGLISH = 'en'
    LANG_CHOICES = (
        (FRENCH, _('French')),
        (ENGLISH, _('English')),
    )   
    # Link FSJUser with a User model for authentication related business
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    
    # All FSJ Users have these attributes in common
    ccid = models.CharField(max_length = 255, unique = True, verbose_name = _("CCID"))
    first_name = models.CharField(max_length = 255, verbose_name = _("First Name"))
    last_name = models.CharField(max_length = 255, verbose_name = _("Last Name"))
    email = models.EmailField(max_length = 254, verbose_name= _("Email"))
    ualberta_id = models.IntegerField(unique = True, verbose_name = _("University of Alberta ID"),
                                      help_text = _("The University of Alberta ID is the Student ID or Employee ID"))
    lang_pref = models.CharField(max_length = 2, blank = False, choices = LANG_CHOICES, default = FRENCH, verbose_name = _("Language Preference"))
    
    def __str__(self):
        return self.ccid
    
    def delete(self, *args, **kwargs):
        # Since we defined cascade delete we don't need to explicitly call super.delete()
        self.user.delete() 