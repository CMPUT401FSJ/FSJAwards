from django.utils.translation import gettext_lazy as _
from django.db import models

class YearOfStudy(models.Model):
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
	year = models.IntegerField(choices = YEAR_CHOICES, verbose_name = _("Year of Study"))

	def __str__(self):
		return self.get_year_display()

