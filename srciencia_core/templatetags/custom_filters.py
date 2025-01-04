from django import template
import re

register = template.Library()

@register.filter
def remove_empty_paragraphs(value):
    return re.sub(r'<p>(\s|&nbsp;)*</p>', '', value)
