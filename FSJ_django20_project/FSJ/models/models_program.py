from django.utils.translation import gettext_lazy as _
from django.db import models

class Program(models.Model):
    class Meta():
        ordering = ('name',)
        
    code = models.CharField(primary_key = True, max_length = 10, verbose_name = _("Code"))
    name = models.CharField(max_length = 255, verbose_name = _("Name"))
    
    def __str__(self):
        return self.name