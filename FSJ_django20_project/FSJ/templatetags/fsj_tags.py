from django import template
from django.template.defaultfilters import stringfilter
from ..models import Application
from ..models import Award
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