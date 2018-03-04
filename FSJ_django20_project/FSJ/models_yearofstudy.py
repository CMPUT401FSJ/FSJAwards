from django.utils.translation import gettext_lazy as _
from django.db import models

class YearOfStudy(models.Model):
	#Choices of year for year of study
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

	#Even if a year is deleted and readded, they will still appear in order
	class Meta:
		ordering = ('year', )

	#years appear as "First", "Second", etc instead of 1, 2, etc 
	def __str__(self):
		return self.get_year_display()

