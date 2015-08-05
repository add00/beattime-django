# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from boards import views

urlpatterns = patterns(
    '',
    url(
        r'^$',
        views.BoardsProfileView.as_view(),
        name='boards-profile'
    ),
    url(
        r'^dashboard$',
        views.BoardsBoardView.as_view(),
        name='boards-board'
    ),
)
