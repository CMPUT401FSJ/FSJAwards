from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime

class Award(models.Model):
	name = models.CharField(max_length = 255, verbose_name = _("Name"))
	description = models.TextField(verbose_name = _("Description"))
	value = models.PositiveIntegerField(verbose_name = _("Value"))
	programs = models.TextField(verbose_name = _("Programs"))
	years_of_study = models.TextField(verbose_name = _("Years of Study"))
	deadline = models.DateTimeField(auto_now = False, auto_now_add = False, verbose_name = _("Deadline"))
	documents_needed = models.BooleanField(verbose_name = _("Documents Required"))
	is_active = models.BooleanField(verbose_name = ("Is Active"))