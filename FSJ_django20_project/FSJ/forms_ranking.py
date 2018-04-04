from .models import Ranking
from .forms_modelform import ModelForm
from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _

class RankingForm(ModelForm):

    class Meta:
        model = Ranking
        fields = ('adjudicator', 'application', 'award', 'score',)
        
    def __init__(self, *args, **kwargs):
        super(RankingForm, self).__init__(*args, **kwargs) 
        rankings = Ranking.objects.filter(adjudicator = user, award = award).values_list('score', flat=True)
        choices = ['--', 1, 2, 3, 4, 5]
        available_rankings = [(("Choice_%s" % str(x)), x) for x in choices if x not in rankings]
        self.fields['score'] = forms.ChoiceField(choices=available_rankings)
        
    def clean_score(self):
        data = self.cleaned_data['score']
        try:
            typename, value = data.split('_')
            score = int(value)
        except ValueError:
            raise ValidationError(_('Cannot understand %s' % data))
        return score  
        
class RankingRestrictedForm(ModelForm):
    
    class Meta:
        model = Ranking
        fields = ('score',)
            
    def __init__(self, user, award, *args, **kwargs):
        super(RankingRestrictedForm, self).__init__(*args, **kwargs)
        rankings = Ranking.objects.filter(adjudicator = user, award = award).values_list('score', flat=True)
        choices = ['--', 1, 2, 3, 4, 5]
        available_rankings = [(("Choice_%s" % str(x)), x) for x in choices if x not in rankings]
        self.fields['score'] = forms.ChoiceField(choices=available_rankings)
        
    def clean_score(self):
        data = self.cleaned_data['score']
        try:
            typename, value = data.split('_')
            score = int(value)
        except ValueError:
            raise ValidationError(_('Cannot understand %s' % data))
        return score    
        
