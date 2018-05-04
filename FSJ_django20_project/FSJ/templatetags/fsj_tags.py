from django import template
from ..models import Application
from ..models import Award

register = template.Library()

@register.simple_tag(takes_context=True)
def get_status(context):
    FSJ_user = context['FSJ_user']
    application = context['application'][0]
    return application.get_status(FSJ_user)


@register.simple_tag(takes_context=True)
def get_review_status(context):
    FSJ_user = context['FSJ_user']
    award = context['award']
    return award.get_review_status(FSJ_user)