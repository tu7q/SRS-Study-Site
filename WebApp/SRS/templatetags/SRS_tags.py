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


@register.filter
def latexnotation(value, digits):
    """
    Turn value into scientific notation
    """
    l = f"{{:.{digits}e}}".format(value).split("e")
    val, exp = l[0], l[1]
    exp = exp.replace("+", "")  # remove + sign
    exp = exp.lstrip("0")  # strip leading 0s
    return f"{val}*10^{{{exp}}}"


# @register.simple_tag(takes_context=True)
# def assesment_GET_params(context, next_page):
#     request = context['request']
#     request
