import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models

class Program(models.Model):
    class Meta():
        ordering = ('name',)
        
    programid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 255, verbose_name = _("Name"))
    
    def __str__(self):
        return self.name