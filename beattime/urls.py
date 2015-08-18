# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin

auth_kwargs = {
    'template_name': 'boards/auth.html'
}

auth_patterns = patterns(
    '',
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        auth_kwargs,
        name='login'
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'
    ),
    url(
        r'^password_change/$',
        'django.contrib.auth.views.password_change',
        auth_kwargs,
        name='password_change'
    ),
    url(
        r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        auth_kwargs,
        name='password_change_done'
    ),
    url(
        r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        auth_kwargs,
        name='password_reset'
    ),
    url(
        r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        auth_kwargs,
        name='password_reset_done'
    ),
    url(
        (
            r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
        ),
        'django.contrib.auth.views.password_reset_confirm',
        auth_kwargs,
        name='password_reset_confirm'
    ),
    url(
        r'^reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        auth_kwargs,
        name='password_reset_complete'
    ),
)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(auth_patterns)),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('boards.urls', namespace='boards'))
)
