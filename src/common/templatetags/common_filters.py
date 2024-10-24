from django import template

register = template.Library()

@register.filter(name='table_header')
def table_header(value):
    """ Replaces all underscores with spaces, removes the word 'datetime', 
        and converts the string to title case. """
    return value.replace("_", " ").replace("datetime", "").title()