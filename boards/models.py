# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from boards import TASK_STATUS
from boards.fields.models import RGBField
from boards.managers import CommentAuthorsManager, StickersManager


COMMENT_LOCATION_LIMIT = (
    models.Q(app_label='boards', model='sticker') |
    models.Q(app_label='boards', model='board')
)


class ConfigurableMixin(models.Model):
    """
    Common methods and attributes.
    @desc: model mixin.
    """
    # @desc: example of property.
    @property
    def stickers(self):
        """
        Returns stickers for given `Board` or `Desk`.
        """
        if isinstance(self, Board):
            return self.boards.sticker_set.all()
        return self.owner.sticker_set.all()

    class Meta:
        abstract = True


class CommonInfo(models.Model):
    """
    Abstract class for models' common information.
    @desc: abstract model class.
    """
    # @desc: foreign key to different app.
    author = models.ForeignKey('profiles.Profile', verbose_name=_('author'))
    # @desc: using of auto_now_add.
    creation_date = models.DateTimeField(
        _('creation_date'), auto_now_add=True, editable=False
    )
    # @desc: using of auto_now.
    modification_date = models.DateTimeField(
        _('creation_date'), auto_now=True, editable=False
    )

    class Meta:
        abstract = True


class Comment(CommonInfo):
    """
    There is a possibility to comment Stickers or Boards. This model store
    all comments.
    """
    # @desc: generic relation.
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(
        ContentType, limit_choices_to=COMMENT_LOCATION_LIMIT
    )
    object_id = models.PositiveIntegerField()

    objects = models.Manager()
    authors_objects = CommentAuthorsManager()

    def __unicode__(self):
        return '@{} [{}]'.format(self.author, self.creation_date)


class Label(models.Model):
    """
    Represents status of task for particular `Sticker` object.
    """
    # @desc: custom field.
    color = RGBField(_('color'))
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return '{} [{}]'.format(self.name, self.color)


class Desk(ConfigurableMixin, models.Model):
    """
    Boards container model.
    """
    # @desc: OneToOne relation.
    owner = models.OneToOneField('profiles.Profile', verbose_name=_('owner'))
    desk_slug = models.SlugField(max_length=5, unique=True)

    def __unicode__(self):
        return self.desk_slug

    @property
    def boards(self):
        """
        Returns boards of particular desk.
        """
        return self.owner.board_set.all()


class Board(ConfigurableMixin, CommonInfo):
    """
    Stickers container model.
    """
    desk = models.ForeignKey(Desk, verbose_name=_('desk'))
    title = models.CharField(_('title'), max_length=100)
    sequence = models.PositiveIntegerField()

    def __unicode__(self):
        return '{} [{}]'.format(self.title, self.desk)

    @property
    def owner_username(self):
        """
        Return owner's username of board, so owner of desk that this board
        is assigned to (not author of board).
        """
        return self.desk.owner.user.username

    class Meta:
        # @desc: unique constrains.
        unique_together = (('desk', 'sequence'),)


class Sticker(CommonInfo):
    """
    Sticker with task description.
    """
    board = models.ForeignKey(Board, verbose_name=_('board'))
    caption = models.CharField(_('caption'), max_length=100)
    # @desc: long text field.
    description = models.TextField(_('description'))
    label = models.ForeignKey(Label, verbose_name=_('label'))
    # @desc: choices field.
    status = models.CharField(_('status'), choices=TASK_STATUS, max_length=1)

    objects = StickersManager()

    @property
    def count_comments(self):
        """
        Return number of comment of a sticker.
        """
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(
            content_type=content_type, object_id=self.pk
        ).count()

    def __unicode__(self):
        return '{} [{}]'.format(self.caption, self.label.name)