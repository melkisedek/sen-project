# -*- coding: UTF-8 -*-
from urllib.parse import urlencode
from django import template
from django.utils.encoding import force_str

register = template.Library()

@register.simple_tag(takes_context=True)
def append_to_query(context, no_path=False, **kwargs):
	# django.core.context_processors.request should be enabled in
    # settings.TEMPLATE_CONTEXT_PROCESSORS.
    # Or else, directly pass the HttpRequest object as 'request' in context.
    query_params = context['request'].GET.copy()
    for key, value in kwargs.items():
        query_params[key] = value
    path = u""
    if len(query_params):
        path += u"?%s" % urlencode([
            (key, force_str(value)) for pair in list(query_params.items()) if value
        ])
    return path