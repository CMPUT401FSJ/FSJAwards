import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models_yearofstudy import *
from datetime import datetime, timezone
from .models_program import Program

class Award(models.Model):
	#All awards will have these attributes in common, will be able to select multiple years of study
	awardid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	award_name = models.CharField(max_length = 255, verbose_name = _("Award Name"))
	description = models.TextField(verbose_name = _("Description"))
	value = models.CharField(max_length = 100, verbose_name = _("Value"))
	programs = models.ManyToManyField(Program, blank = True, verbose_name = _("Programs"))
	years_of_study = models.ManyToManyField(YearOfStudy, verbose_name = _("Years"))
	start_date = models.DateTimeField(auto_now = False, auto_now_add = False, verbose_name = _("Start date"))
	end_date = models.DateTimeField(auto_now = False, auto_now_add = False, verbose_name = _("End Date"))
	documents_needed = models.BooleanField(verbose_name = _("Documents Required"))
	is_active = models.BooleanField(verbose_name = _("Is Active"))

	#returns award name as a string
	def __str__(self):
		return self.award_name

	#returns a bool stating whether the award is open or not due to start/end date
	def is_open(self):
		now = datetime.now(timezone.utc)
		if self.start_date > now or self.end_date < now:
			return False
		else:
			return True
