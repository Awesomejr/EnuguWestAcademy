from django import template

register = template.Library()

@register.filter
def floatdiv(value, arg):
    """Divides the value by the argument and returns the result."""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)