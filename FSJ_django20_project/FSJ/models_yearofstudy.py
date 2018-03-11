from django.utils.translation import gettext_lazy as _
from django.db import models

class YearOfStudy(models.Model):
	#Choices of year for year of study
	year = models.CharField(max_length = 255, unique = True, verbose_name = _("Year of Study"))

	def __str__(self):
		return self.year

