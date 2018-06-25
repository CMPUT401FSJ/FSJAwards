from django import template
from django.template.defaultfilters import stringfilter
from ..models import Ranking
from ..forms import AwardReviewCommentForm
import urllib
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def get_status(context):
    """Gets the review status of an application"""
    FSJ_user = context['FSJ_user']
    application = context['application']
    return application.get_status(FSJ_user)

@register.simple_tag(takes_context=True)
def get_status_tuple(context):
    """Gets the review status of an application which has been zipped into a tuple"""
    FSJ_user = context['FSJ_user']
    application = context['application'][0]
    return application.get_status(FSJ_user)


@register.simple_tag(takes_context=True)
def get_review_status(context):
    """Gets the review status of an award"""
    FSJ_user = context['FSJ_user']
    award = context['award']
    return award.get_review_status(FSJ_user)

@register.filter
@stringfilter
def quote(value):
    """Gets a string and returns the encoded value

    value -- the string to be encoded
    """
    return urllib.parse.quote(value)

@register.filter
@stringfilter
def unquote(value):
    """Gets a string and returns the decoded value

    value -- the string to be decoded
    """
    return urllib.parse.unquote(value)

@register.simple_tag(takes_context=True)
def get_ranking(context, rank):
    """Gets the ranking of a particular value for a given award and adjudicator

    rank -- the ranking value
    """
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
    """An unused tag from experimentation with forms"""
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
    """returns a range spanning from 1 to size

    size -- number of elements in the range
    """
    return range(1, size+1)

@register.filter
def get_range_0(size):
    """returns a range spanning from 0 to size-1

    size -- number of elements in the range
    """
    return range(0, size)

@register.simple_tag(takes_context=True)
def get_award_id(context):
    """Experimental and no longer needed"""
    awards_list = context['awards_list']
    x = context['x']
    award = awards_list[x]

    return award.awardid

@register.filter(name='link_name')
def link_name(path, page_number):
    """Code sourced from https://medium.com/@sumitlni/paginate-properly-please-93e7ca776432
    Changes the page number in a url to page_number

    path -- the url to be changed
    page_number -- the number of the page to be inserted
    """
    output = re.search('(page=\d+)', path)
    if output is not None:
        return path.replace(str(output.group(1)), "page=" + str(page_number))
    if re.search('(page=\d+)', path):
        path.replace()
    page_number = str(page_number)
    if '?' in path:
        return path + "&page=" + page_number
    return path + "?page=" + page_number

@register.filter(name='proper_paginate')
def proper_paginate(paginator, current_page, neighbors=5):
    """Code sourced from https://medium.com/@sumitlni/paginate-properly-please-93e7ca776432
    Gets the range of pages surrounding the current page

    current_page -- page number of the current page
    neighbors -- number of neighbors to get on either side of current page
    """
    if paginator.num_pages > 2*neighbors:
        start_index = max(1, current_page-neighbors)
        end_index = min(paginator.num_pages, current_page + neighbors)
        page_list = [f for f in range(start_index, end_index+1)]
        return page_list[:(2*neighbors + 1)]
    return paginator.page_range