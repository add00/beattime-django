from django.template import Library

register = Library()


@register.filter
def range(to, _from=1):
    """
    Return list of numbers for loop purposes
    """
    to += 1
    return xrange(_from, to)
