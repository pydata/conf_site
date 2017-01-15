from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

import markdown as markdown_library


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    """<https://www.dominicrodger.com/2013/01/16/django-markdown/>"""
    extensions = ["nl2br", ]

    return mark_safe(
        markdown_library.markdown(
            force_unicode(value),
            extensions,
            safe_mode=True,
            enable_attributes=False
        )
    )
