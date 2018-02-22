#from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from .forms import AddAwardForm
from django.forms import *
from django.db import models
import datetime

class Award(models.Model):
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
	value = models.PositiveIntegerField(verbose_name = _("Value"))
	programs = models.TextField(verbose_name = _("Programs"))
	years_of_study = models.IntegerField(choices = YEAR_CHOICES, verbose_name = _("Years of Study"))
	deadline = models.DateTimeField(auto_now = False, auto_now_add = False, verbose_name = _("Deadline"))
	documents_needed = models.BooleanField(verbose_name = _("Documents Required"))
	#document = models.FileField(upload_to = None, max_length = 100, verbose_name = _("Documents"))
	is_active = models.BooleanField(verbose_name = ("Is Active"))


	def __str__(self):
		return self.award_name

	def get_add_award_form(self, request = None):
		if request and request.POST:
			add_award_form = CoordinatorAddAwardForm(request.POST)
		else:
			add_award_form = CoordinatorAddAwardForm()
		return add_award_form

	def get_award_id(self):
		return awardid

class CoordinatorAddAwardForm(AddAwardForm):
	award_id = IntegerField()
       
	def __init__(self, *args, **kwargs):
		super(AddAwardForm, self).__init__(*args, **kwargs)           
		self.fields['award_id'].disabled = True