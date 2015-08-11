from django.core.urlresolvers import resolve
from django.template import Library

register = Library()


@register.simple_tag()
def active_page(request, name):
    """
    Return `active` if current page equals given url name.
    """
    url_name = resolve(request.path).url_name
    return 'active' if url_name == name else ''
