# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
import random
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beattime.settings')
django.setup()

from profiles.models import *
from boards.models import *
from django.contrib.auth.models import User

OPEN = 'OPEN'
IN_PROGRESS = 'PROGRESS'
IN_REVIEW = 'REVIEW'
DONE = 'DONE'
BLOCKED = 'BLOCKED'

STATUSES = [OPEN, IN_PROGRESS, IN_REVIEW, DONE]  # , BLOCKED]

CSS_CLASS = (
    ('bg-todo', OPEN),
    ('bg-inprogress', IN_PROGRESS),
    ('bg-inreview', IN_REVIEW),
    ('bg-done', DONE),
    ('bg-blocked', BLOCKED)
)


def prepare_user(seq):
    u_slug = 'u{}'.format(seq)
    d_slug = 'd{}'.format(seq)
    mail = '{}@test.com'.format(u_slug)

    user = User.objects.create_superuser(u_slug, mail, u_slug)
    profile, _ = Profile.objects.get_or_create(display_name=u_slug, user=user)
    desk, _ = Desk.objects.get_or_create(owner=profile, desk_slug=d_slug)

    return profile, desk


def process(author, desk):
    for seq_b in range(5):
        b, _ = Board.objects.get_or_create(
            author=author, desk=desk, title='board{}'.format(seq_b),
            sequence=seq_b, prefix='TEST{}'.format(seq_b),
        )
        for seq in range(5):
            Sticker.objects.get_or_create(
                author=author, board=b, caption='stick{}'.format(seq),
                description='desc{}'.format(seq),
                label=Label.objects.get(status=random.choice(STATUSES)),
                sequence=seq
            )


def create_labels():
    for css_class, status in CSS_CLASS:
        Label.objects.get_or_create(
            color='#eee', css_class=css_class, status=status
        )


create_labels()

p1, d1 = prepare_user(1)  # Profile 1
process(p1, d1)

p2, d2 = prepare_user(2)  # Profile 2
process(p2, d2)
