from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class FSJUser(models.Model):
    # List the languages a user may choose from in human readable format and also make them accessible in other files 
    # via FSJUser.LANG_CHOICES, FSJUser.ENGLISH, etc.
    FRENCH = 'fr'
    ENGLISH = 'en'
    LANG_CHOICES = (
        (FRENCH, "Fran"+u"\u00E7"+"ais"),
        (ENGLISH, 'English'),
    )   
    # Link FSJUser with a User model for authentication related business
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True, null = True)    
    
    # All FSJ Users have these attributes in common
    ccid = models.CharField(max_length = 255, unique = True, verbose_name = _("CCID"))
    first_name = models.CharField(max_length = 255, verbose_name = _("First Name"))
    last_name = models.CharField(max_length = 255, verbose_name = _("Last Name"))
    email = models.EmailField(max_length = 254, verbose_name= _("Email"))
    lang_pref = models.CharField(max_length = 2, blank = False, choices = LANG_CHOICES, default = FRENCH, verbose_name = _("Language Preference"))
    
    def __str__(self):
        return self.ccid
    

    # The user class for a base FSJUSer is nonexistent. This method needs to be overridden by classes that inherit from it
    def user_class(self):
        return None

    def get_name(self):
        return self.first_name + ' ' + self.last_name

    @transaction.atomic # The method is an atomic transaction so if something occurs part way through it will not persist the User.
    def save(self, *args, **kwargs):
        if not self.user:
            user = User()
            user.username = self.ccid
            user.email = self.email
            user.save()
            self.user = user
        else:
            self.user.email = self.email
            self.user.username = self.ccid
            self.user.save()
        super(FSJUser, self).save(*args, **kwargs)   
        
    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super(FSJUser, self).delete(*args, **kwargs)

