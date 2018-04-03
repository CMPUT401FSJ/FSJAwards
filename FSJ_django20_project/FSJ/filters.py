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
	last_name = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Student
		fields = ['ccid','first_name','last_name','year','program']

#TODO: add fields 'assigned awards' and 'committee'
class AdjudicatorFilter(django_filters.FilterSet):
	ccid = django_filters.CharFilter(lookup_expr='icontains')
	first_name = django_filters.CharFilter(lookup_expr='icontains')
	last_name = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Adjudicator
		fields = ['ccid','first_name','last_name']

class AwardFilter(django_filters.FilterSet):
	award_name = django_filters.CharFilter(lookup_expr='icontains')
	description = django_filters.CharFilter(lookup_expr='icontains')
	start_date = django_filters.DateFilter(widget = DateInput())
	end_date = django_filters.DateFromToRangeFilter(widget = DateInput())

	class Meta:
		model = Award
		fields = ['award_name','description','value','programs','years_of_study','start_date', 'end_date', 'documents_needed','is_active']