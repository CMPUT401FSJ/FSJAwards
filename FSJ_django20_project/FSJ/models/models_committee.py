import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models_adjudicator import *
from .models_award import *

class Committee(models.Model):
	#All committees will have these attributes in common
	committeeid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	committee_name = models.CharField(max_length=255, verbose_name = _("Committee Name"))
	adjudicators = models.ManyToManyField(Adjudicator, related_name='committees', verbose_name = _("Adjudicators"))
	awards = models.ManyToManyField(Award, related_name='committees', verbose_name = _("Awards"))
	
	def __str__(self):
		return self.committee_name