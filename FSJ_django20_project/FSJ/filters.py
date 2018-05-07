from .models import *
import django_filters
from django.forms import CheckboxSelectMultiple, DateInput
from django.utils.translation import gettext_lazy as _

LOOKUP_TYPES = [
        ('icontains', _("contains"))
]

class DateInput(DateInput):
	input_type = 'date'


class StudentFilter(django_filters.FilterSet):
	ccid = django_filters.CharFilter(lookup_expr='icontains')
	first_name = django_filters.CharFilter(lookup_expr='icontains')
	middle_name = django_filters.CharFilter(lookup_expr='icontains')
	last_name = django_filters.CharFilter(lookup_expr='icontains')
	student_id = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Student
		fields = ['ccid','first_name','middle_name','last_name','student_id','year','program']

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
	student_ccid = django_filters.CharFilter(name='student__ccid', lookup_expr='icontains')
	student_first_name = django_filters.CharFilter(name='student__first_name', lookup_expr='icontains')
	student_last_name = django_filters.CharFilter(name='student__last_name', lookup_expr='icontains')
	award_name = django_filters.CharFilter(name='award__name', lookup_expr='icontains')
	
	class Meta:
		model = Application
		fields = ['award', 'award__programs', 'is_submitted']