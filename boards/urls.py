# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, patterns, url
from django.contrib.auth.decorators import login_required

from boards import views


sprint_patterns = patterns(
    '',
    url(
        r'^new/$',
        login_required(views.SprintCreate.as_view()),
        name='sprint-create'
    ),
    url(
        r'^(?P<sprint_number>[0-9]{1,5}.[0-9]{2})/', include([
            url(
                r'^$',
                login_required(views.SprintDetail.as_view()),
                name='sprint-detail'
            ),
            url(
                r'^comments/$',
                login_required(views.SprintComments.as_view()),
                name='sprint-comments'
            ),
        ])
    ),
)

board_patterns = patterns(
    '',
    url(
        r'^new/$',
        login_required(views.BoardCreate.as_view()),
        name='board-create'
    ),
    url(
        r'^(?P<board_sequence>[0-9]+)/', include([
            url(
                r'^$',
                login_required(views.BoardDetail.as_view()),
                name='board-detail'
            ),
            url(
                r'^comments/$',
                login_required(views.BoardComments.as_view()),
                name='board-comments'
            ),
            url(r'^sprint/', include(sprint_patterns))
        ])
    ),
)

sticker_patterns = patterns(
    '',
    url(
        (
            r'^new/board/(?P<board_sequence>[0-9]+)'
            r'(?:/sprint/(?P<sprint_number>[0-9]{1,5}.[0-9]{2}))?/$'
        ),
        login_required(views.StickerCreate.as_view()),
        name='sticker-create'
    ),
    url(
        r'^(?P<prefix>[-a-zA-Z0-9_]{1,5})-(?P<sequence>[0-9]+)/', include([
            url(
                r'^$',
                login_required(views.StickerDetail.as_view()),
                name='sticker-detail'
            ),
            url(
                r'^update/$',
                login_required(views.StickerUpdate.as_view()),
                name='sticker-update'
            ),
        ])
    ),
)

urlpatterns = patterns(
    '',
    url(
        r'^(?:user/(?P<username>[a-z0-9_-]+)/)?$',
        login_required(views.ProfileDetail.as_view()),
        name='profile-detail'
    ),
    url(
        r'^(?:user/(?P<username>[a-z0-9_-]+)/)?board/',
        include(board_patterns)
    ),
    url(
        r'^(?:user/(?P<username>[a-z0-9_-]+)/)?sticker/',
        include(sticker_patterns)
    ),
)
