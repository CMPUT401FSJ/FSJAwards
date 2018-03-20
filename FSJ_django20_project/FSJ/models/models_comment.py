import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models_application import Application
from .models_FSJUser import FSJUser

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='comments', verbose_name = _("Application"))
    adjudicator = models.ForeignKey(FSJUser, on_delete=models.CASCADE, related_name='comments', to_field='ccid', verbose_name = _("Adjudicator"))
    comment_text = models.CharField(max_length = 255, unique = True, verbose_name = _("Comment Text"))
    
    
    def __str__(self):
        return comment_text   
    