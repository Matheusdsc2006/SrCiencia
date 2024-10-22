from django import template

register = template.Library()

@register.filter
def add_attrs(field, css):
    attrs = {}
    definition = css.split(',')
    for d in definition:
        key, value = d.split('=')
        attrs[key] = value
    return field.as_widget(attrs=attrs)
