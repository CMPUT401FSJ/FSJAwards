from .models import Ranking
from .forms_modelform import ModelForm
from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

class RankingForm(ModelForm):

    class Meta:
        model = Ranking
        fields = ('adjudicator', 'application', 'award', 'rank',)
        
    def __init__(self, *args, **kwargs):
        super(RankingForm, self).__init__(*args, **kwargs) 
        rankings = Ranking.objects.filter(adjudicator = user, award = award)
        if self.instance.pk is not None:
            rankings = rankings.exclude(pk=self.instance.pk).values_list('rank', flat=True)        
        choices = ['--', 1, 2, 3, 4, 5]
        available_rankings = [(str(x), x) for x in choices if x not in rankings]
        self.fields['rank'] = forms.ChoiceField(choices=available_rankings)
        
    def clean_rank(self):
        data = self.cleaned_data['rank']
        try:
            rank = int(data)
        except ValueError:
            raise ValidationError(_('Cannot understand %s' % data))
        return rank  
        
class RankingRestrictedForm(ModelForm):
    
    class Meta:
        model = Ranking
        fields = ('rank',)
            
    def __init__(self, user, award, *args, **kwargs):
        super(RankingRestrictedForm, self).__init__(*args, **kwargs)
        rankings = Ranking.objects.filter(adjudicator = user, award = award)
        if self.instance.pk is not None:
            rankings = rankings.exclude(pk=self.instance.pk).values_list('rank', flat=True)         
        choices = ['--', 1, 2, 3, 4, 5]
        available_rankings = [(str(x), x) for x in choices if x not in rankings]
        self.fields['rank'] = forms.ChoiceField(choices=available_rankings)
        
    def clean_rank(self):
        data = self.cleaned_data['rank']
        try:
            rank = int(data)
        except ValueError:
            raise ValidationError(_('Cannot understand %s' % data))
        return rank    
        
