# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from boards import views

urlpatterns = patterns(
    '',
    url(
        r'^(?:(?P<username>[a-z0-9_-]+)/)?$',
        views.ProfileView.as_view(),
        name='boards-profile'
    ),
    url(
        r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)$',
        views.BoardView.as_view(),
        name='boards-board'
    ),
    url(
        (
            r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?'
            r'(?P<prefix>[-a-zA-Z0-9_]{1,5})-(?P<sequence>[0-9]+)$'
        ),
        views.StickerDetail.as_view(),
        name='boards-sticker-detail'
    ),
    url(
        r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)$',
        views.StickerCreate.as_view(),
        name='boards-sticker-create'
    ),
    url(
        (
            r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?'
            r'(?P<prefix>[-a-zA-Z0-9_]{1,5})-(?P<sequence>[0-9]+)/update$'
        ),
        views.StickerUpdate.as_view(),
        name='boards-sticker-update'
    ),
)
