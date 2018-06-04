from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid

class YearOfStudy(models.Model):
	"""Represents a university year of study"""

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	year = models.CharField(max_length = 255, unique = True, verbose_name = _("Year of Study"))

	def __str__(self):
		return self.year
