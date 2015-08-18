# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from profiles import FORBIDDEN_USERNAMES


def get_user(request, kwargs):
    """
    Return user basing on request.
    """
    username = kwargs.get('username')
    if username in FORBIDDEN_USERNAMES:
        raise Http404('Given user does not exist')
    elif username:
        return get_object_or_404(User, username=kwargs['username'])
    return request.user
