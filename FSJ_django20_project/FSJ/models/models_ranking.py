from django.db import models
from .models_award import Award
from .models_application import Application
from .models_adjudicator import Adjudicator
from django.utils.translation import gettext_lazy as _

class Ranking(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='rankings', verbose_name = _("Award"))
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='rankings', verbose_name = _("Application"))
    adjudicator = models.ForeignKey(Adjudicator, on_delete=models.CASCADE, related_name='rankings', verbose_name = _("Adjudicator"))
    score = models.IntegerField(null = True, blank = True, verbose_name = _("Rank"))

    class Meta:
        unique_together = ('award', 'adjudicator', 'score',)