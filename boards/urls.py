# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from boards import views

urlpatterns = patterns(
    '',
    url(
        r'^$',
        views.ProfileView.as_view(),
        name='boards-profile'
    ),
    url(
        r'^dashboard/(?P<username>[a-z0-9_-]+)/(?P<board_sequence>[0-9]+)$',
        views.BoardView.as_view(),
        name='boards-board'
    ),
)
