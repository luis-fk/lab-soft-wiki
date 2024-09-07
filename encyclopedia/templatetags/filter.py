from django import template

register = template.Library()

@register.filter
def replaceHyphensWithSpaces(value):
    return value.replace('-', ' ')
