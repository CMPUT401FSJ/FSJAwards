import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
import datetime

class Award(models.Model):
	#All awards will have these attributes in common, will be able to select multiple years of study
	FIRST = 1
	SECOND = 2
	THIRD = 3
	FOURTH = 4
	FIFTH = 5
	YEAR_CHOICES = (
		(FIRST, _('First')),
		(SECOND, _('Second')),
		(THIRD, _('Third')),
		(FOURTH, _('Fourth')),
		(FIFTH, _('Fifth'))
	)
	awardid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	award_name = models.TextField(verbose_name = _("Award Name"))
	description = models.TextField(verbose_name = _("Description"))
	value = models.TextField(verbose_name = _("Value"))
	programs = models.TextField(verbose_name = _("Programs"))
	years_of_study = models.IntegerField(choices = YEAR_CHOICES, verbose_name = _("Years of Study"))
	deadline = models.DateTimeField(auto_now = False, auto_now_add = False, verbose_name = _("Deadline"))
	documents_needed = models.BooleanField(verbose_name = _("Documents Required"))
	is_active = models.BooleanField(verbose_name = ("Is Active"))

	#returns award name as a string
	def __str__(self):
		return self.award_name

	def get_year_name(self):
		return self.get_years_of_study_display()