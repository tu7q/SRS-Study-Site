import itertools

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def absurl(context, url, **kwargs):
    request = context["request"]
    return request.build_absolute_uri(reverse(url, kwargs=kwargs))


@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break


# @register.simple_tag(takes_context=True)
# def assesment_GET_params(context, next_page):
#     request = context['request']
#     request
