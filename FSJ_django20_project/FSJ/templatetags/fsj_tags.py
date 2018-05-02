from django import template
from ..models import Application

register = template.Library()

@register.simple_tag(takes_context=True)
def get_adj_status(context):
    FSJ_user = context['FSJ_user']
    application = context['application'][0]
    return application.get_adj_status(FSJ_user)
