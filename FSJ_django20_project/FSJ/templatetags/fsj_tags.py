from django import template
from django.template.defaultfilters import stringfilter
from ..models import Ranking
from ..forms import AwardReviewCommentForm
import urllib

register = template.Library()

@register.simple_tag(takes_context=True)
def get_status(context):
    FSJ_user = context['FSJ_user']
    application = context['application']
    return application.get_status(FSJ_user)

@register.simple_tag(takes_context=True)
def get_status_tuple(context):
    FSJ_user = context['FSJ_user']
    application = context['application'][0]
    return application.get_status(FSJ_user)


@register.simple_tag(takes_context=True)
def get_review_status(context):
    FSJ_user = context['FSJ_user']
    award = context['award']
    return award.get_review_status(FSJ_user)

@register.filter
@stringfilter
def quote(value):
    return urllib.parse.quote(value)

@register.filter
@stringfilter
def unquote(value):
    return urllib.parse.unquote(value)

@register.simple_tag(takes_context=True)
def get_ranking(context, rank):
    award = context['award']
    adjudicator = context['adjudicator']
    try:
        ranking = Ranking.objects.get(award=award, adjudicator=adjudicator, rank=rank)
        ccid = ranking.application.student.ccid
        return ccid

    except:
        return ""

@register.simple_tag(takes_context=True)
def get_ranking_x(context, rank):
    awards_list = context['awards_list']
    adjudicator = context['adjudicator']
    x = context['x']
    try:
        ranking = Ranking.objects.get(award=awards_list[x], adjudicator=adjudicator, rank=rank)
        ccid = ranking.application.student.ccid
        return ccid

    except:
        return ""


@register.filter
def get_range(size):
    return range(1, size+1)

@register.filter
def get_range_0(size):
    return range(0, size)

@register.simple_tag(takes_context=True)
def get_award_id(context):
    awards_list = context['awards_list']
    x = context['x']
    award = awards_list[x]

    return award.awardid