from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def absurl(context, url, **kwargs):
    request = context["request"]
    return request.build_absolute_uri(reverse(url, kwargs=kwargs))
