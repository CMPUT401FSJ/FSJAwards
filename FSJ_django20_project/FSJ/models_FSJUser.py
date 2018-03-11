from django.db import models
from django.utils.translation import gettext_lazy as _

class FSJUser(models.Model):
    # List the languages a user may choose from in human readable format and also make them accessible in other files 
    # via FSJUser.LANG_CHOICES, FSJUser.ENGLISH, etc.
    FRENCH = 'fr'
    ENGLISH = 'en'
    LANG_CHOICES = (
        (FRENCH, _('French')),
        (ENGLISH, _('English')),
    )   
     # All FSJ Users have these attributes in common
    ccid = models.CharField(max_length = 255, unique = True, verbose_name = _("CCID"))
    first_name = models.CharField(max_length = 255, verbose_name = _("First Name"))
    last_name = models.CharField(max_length = 255, verbose_name = _("Last Name"))
    email = models.EmailField(max_length = 254, verbose_name= _("Email"))
    userid = models.IntegerField()
    lang_pref = models.CharField(max_length = 2, blank = False, choices = LANG_CHOICES, default = FRENCH, verbose_name = _("Language Preference"))
    
    def __str__(self):
        return self.ccid
    
    # The user class for a base FSJUSer is nonexistent. This method needs to be overridden by classes that inherit from it
    def user_class(self):
        return None