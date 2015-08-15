# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from boards import views

urlpatterns = patterns(
    '',
    url(
        r'^(?:(?P<username>[a-z0-9_-]+)/)?$',
        views.ProfileDetail.as_view(),
        name='profile-detail'
    ),
    url(
        r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)$',
        views.BoardDetail.as_view(),
        name='board-detail'
    ),
    url(
        r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)/comments$',
        views.BoardComments.as_view(),
        name='board-comments'
    ),
    url(
        (
            r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?'
            r'(?P<prefix>[-a-zA-Z0-9_]{1,5})-(?P<sequence>[0-9]+)$'
        ),
        views.StickerDetail.as_view(),
        name='sticker-detail'
    ),
    url(
        r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)$',
        views.StickerCreate.as_view(),
        name='sticker-create'
    ),
    url(
        (
            r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?'
            r'(?P<prefix>[-a-zA-Z0-9_]{1,5})-(?P<sequence>[0-9]+)/update$'
        ),
        views.StickerUpdate.as_view(),
        name='sticker-update'
    ),
)
