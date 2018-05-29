import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models_yearofstudy import *
from datetime import datetime
import pytz
from .models_program import Program
from .models_adjudicator import Adjudicator

class Award(models.Model):
	# All awards will have these attributes in common, will be able to select multiple years of study
	awardid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length = 255, verbose_name = _("Name"))
	description = models.TextField(verbose_name = _("Description"))
	value = models.CharField(max_length = 100, verbose_name = _("Value"))
	programs = models.ManyToManyField(Program, blank = True, verbose_name = _("Programs"))
	years_of_study = models.ManyToManyField(YearOfStudy, blank = True, verbose_name = _("Years"))
	start_date = models.DateTimeField(auto_now = False, auto_now_add = False, verbose_name = _("Start date"))
	end_date = models.DateTimeField(auto_now = False, auto_now_add = False, verbose_name = _("End Date"))
	documents_needed = models.BooleanField(verbose_name = _("Documents Required"))
	is_active = models.BooleanField(verbose_name = _("Is Active"))
	adjudicators = models.ManyToManyField(Adjudicator, related_name='awards', verbose_name = _("Adjudicators"))
	review_comment = models.CharField(blank = True, max_length = 255, verbose_name = _("Comment"))

	#returns award name as a string
	def __str__(self):
		return self.name

	#returns a bool stating whether the award is open or not due to start/end date
	def is_open(self):
		now = datetime.now(pytz.timezone('America/Edmonton'))
		if self.start_date > now or self.end_date < now:
			return False
		else:
			return True


	def get_review_status(self, FSJ_user):

		if self.applications.count() == 0:
			return "No Applications"

		if FSJ_user.user_class() == "Coordinator":
			applications = self.applications.all()
			need_review = 0
			reviewed = 0
			for application in applications:

				if application.is_reviewed:
					reviewed += 1
				else:
					need_review += 1

			if reviewed == 0 and need_review >= 1:
				return _("Review Required")

			elif reviewed >= 1 and need_review >= 1:
				return _("Review In Progress")

			elif reviewed >= 1 and need_review == 0:
				return _("Review Completed")

		elif FSJ_user.user_class() == "Adjudicator":
			if FSJ_user in self.adjudicators.all():
				return _("Review Completed")
			else: 
				applications = self.applications.all()
				need_review = 0
				for application in applications:
					
					if not application.is_adj_reviewed(FSJ_user):
						need_review += 1
						
				if need_review == applications.count():
					return _("Review Required")
				else:
					return _("Review In Progress")
			




	def add_reviewed(self, FSJ_user):
		if FSJ_user not in self.adjudicators.all():
			self.adjudicators.add(FSJ_user)            

	def delete_reviewed(self, FSJ_user):
		try:
			self.adjudicators.filter(pk = FSJ_user.pk).delete()

		except:
			pass        	
		
		
	def reset(self, new_start_date, new_end_date):
		
		self.applications.all().delete()
		self.adjudicators.all().delete()
		if new_start_date:
			self.start_date = new_start_date
		if new_end_date:
			self.end_date = new_end_date
			
	def change_date(self, new_start_date, new_end_date):
		
		if new_start_date:
			self.start_date = new_start_date
		if new_end_date:
			self.end_date = new_end_date	


	def get_start_date(self):
		return

	def all_archived(self):
		for application in self.applications.all():
			if not application.is_archived:
				return False

		return True