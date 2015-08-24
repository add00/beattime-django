# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from boards import views


urlpatterns = patterns(
    '',
    url(
        r'^(?:(?P<username>[a-z0-9_-]+)/)?$',
        login_required(views.ProfileDetail.as_view()),
        name='profile-detail'
    ),
    url(
        r'^board/(?:(?P<username>[a-z0-9_-]+)/)?new/$',
        login_required(views.BoardCreate.as_view()),
        name='board-create'
    ),
    url(
        r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)$',
        login_required(views.BoardDetail.as_view()),
        name='board-detail'
    ),
    url(
        r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)/comments$',
        login_required(views.BoardComments.as_view()),
        name='board-comments'
    ),
    url(
        (
            r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)'
            r'/sprint/new/$'
        ),
        login_required(views.SprintCreate.as_view()),
        name='sprint-create'
    ),
    url(
        (
            r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)'
            r'/sprint/(?P<sprint_number>[0-9]{1,5}.[0-9]{2})/$'
        ),
        login_required(views.SprintDetail.as_view()),
        name='sprint-detail'
    ),
    url(
        (
            r'^board/(?:(?P<username>[a-z0-9_-]+)/)?(?P<board_sequence>[0-9]+)'
            r'/sprint/(?P<sprint_number>[0-9]{1,5}.[0-9]{2})/comments$'
        ),
        login_required(views.SprintComments.as_view()),
        name='sprint-comments'
    ),
    url(
        (
            r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?'
            r'(?P<prefix>[-a-zA-Z0-9_]{1,5})-(?P<sequence>[0-9]+)$'
        ),
        login_required(views.StickerDetail.as_view()),
        name='sticker-detail'
    ),
    url(
        (
            r'^(?:(?P<username>[a-z0-9_-]+)/)?board/(?P<board_sequence>[0-9]+)'
            r'(?:/sprint/(?P<sprint_number>[0-9]{1,5}.[0-9]{2}))?/sticker/new/?$'
        ),
        login_required(views.StickerCreate.as_view()),
        name='sticker-create'
    ),
    url(
        (
            r'^sticker/(?:(?P<username>[a-z0-9_-]+)/)?'
            r'(?P<prefix>[-a-zA-Z0-9_]{1,5})-(?P<sequence>[0-9]+)/update$'
        ),
        login_required(views.StickerUpdate.as_view()),
        name='sticker-update'
    ),
)
