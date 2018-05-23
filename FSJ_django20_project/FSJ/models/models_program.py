from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid


class Program(models.Model):
    class Meta():
        ordering = ('name',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length = 10, unique=True, verbose_name = _("Code"))
    name = models.CharField(max_length = 255, verbose_name = _("Name"))
    
    def __str__(self):
        return self.name