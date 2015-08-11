from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def get_user(request, kwargs):
    """
    Return user basing on request.
    """
    if kwargs.get('username'):
        return get_object_or_404(User, username=kwargs['username'])
    return request.user
