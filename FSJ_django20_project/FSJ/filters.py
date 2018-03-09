from .models_FSJUser import FSJUser
import django_filters

class UserFilter(django_filters.FilterSet):
	#allow for filtering based on partial search
	first_name = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = FSJUser
		fields = ['ccid','first_name','last_name','email']
