# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    """
    Users' model.
    """
    display_name = models.CharField(_('display_name'), max_length=100)
    # @desc: self and a ManyToMany relation.
    friends = models.ManyToManyField(
        'self', blank=True, verbose_name=_('friends')
    )
    user = models.OneToOneField(User, verbose_name=_('user'))

    def save(self, *args, **kwargs):
        """
        Initialize `display_name` when its empty.
        """
        if not self.display_name and self.user.username:
            self.display_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.display_name


class ActivityType(models.Model):
    """
    Each activity ('Activities' record) has its own type. This model
    is intended to store these kind of data.
    """
    description = models.CharField(
        _('description'), blank=True, max_length=255, null=True,
    )
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return self.name


class Activities(models.Model):
    """
    Model to store users' activities of different types (defined in
    `ActivityType`).
    """
    what = models.ForeignKey(ActivityType, verbose_name=_('what'))
    when = models.DateTimeField(
        _('when'), auto_now_add=True, editable=False
    )
    who = models.ForeignKey(Profile, verbose_name=_('who'))

    def __unicode__(self):
        return '@{} - {} [{}]'.format(self. who, self.what, self.when)
