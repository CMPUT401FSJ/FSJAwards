from .models import *
import django_filters
from django.forms import CheckboxSelectMultiple, DateInput
from django.utils.translation import gettext_lazy as _

LOOKUP_TYPES = [
        ('icontains', _("contains"))
]

class DateInput(DateInput):
	input_type = 'date'
	template_name = 'FSJ/date_field.html'

class StudentFilter(django_filters.FilterSet):
	ccid = django_filters.CharFilter(label=_("CCID contains:"), lookup_expr='icontains')
	first_name = django_filters.CharFilter(label=_("First Name contains:"), lookup_expr='icontains')
	middle_name = django_filters.CharFilter(label=_("Middle Name contains:"), lookup_expr='icontains')
	last_name = django_filters.CharFilter(label=_("Last Name contains:"), lookup_expr='icontains')
	student_id = django_filters.CharFilter(label =_("Student ID contains:"), lookup_expr='icontains')

	class Meta:
		model = Student
		fields = ['ccid','first_name','middle_name','last_name','student_id','year','program']

	def __init__(self, *args, **kwargs):
		super(StudentFilter, self).__init__(*args, **kwargs)
		self.filters['year'].label = _("Year:")
		self.filters['program'].label = _("Program:")


#TODO: add fields 'assigned awards' and 'committee'
class AdjudicatorFilter(django_filters.FilterSet):
	ccid = django_filters.CharFilter(lookup_expr='icontains')
	first_name = django_filters.CharFilter(lookup_expr='icontains')
	last_name = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Adjudicator
		fields = ['ccid','first_name','last_name']

class AwardFilter(django_filters.FilterSet):
	name = django_filters.CharFilter(lookup_expr='icontains')
	description = django_filters.CharFilter(lookup_expr='icontains')
	start_date = django_filters.DateFilter(widget = DateInput())
	end_date = django_filters.DateFilter(widget = DateInput())

	class Meta:
		model = Award
		fields = ['name','description','value','programs','years_of_study','start_date', 'end_date', 'documents_needed','is_active']
		
class ApplicationFilter(django_filters.FilterSet):
	student_ccid = django_filters.CharFilter(name='student__ccid', label=_("Student CCID contains:"), lookup_expr='icontains')
	student_first_name = django_filters.CharFilter(name='student__first_name', label=_("Student First Name contains:"), lookup_expr='icontains')
	student_last_name = django_filters.CharFilter(name='student__last_name', label=_("Student Last Name contains:"), lookup_expr='icontains')
	award_name = django_filters.CharFilter(name='award__name', label=_("Award Name contains:"), lookup_expr='icontains')
	
	class Meta:
		model = Application
		fields = ['award', 'award__programs', 'is_submitted', 'is_archived', 'is_reviewed']

	def __init__(self, *args, **kwargs):
		super(ApplicationFilter, self).__init__(*args, **kwargs)
		self.filters['award'].label = _("Award:")
		self.filters['award__programs'].label = _("Award Programs:")
		self.filters['is_submitted'].label = _("Is Submitted:")
		self.filters['is_archived'].label = _("Is Archived:")
		self.filters['is_reviewed'].label = _("Is Reviewed:")