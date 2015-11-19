# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from boards import CSS_CLASS, TASK_STATUS
from boards.fields.models import RGBField
from boards.managers import CommentAuthorsManager, StickersManager

from profiles.models import Profile


COMMENT_LOCATION_LIMIT = (
    models.Q(app_label='boards', model='board') |
    models.Q(app_label='boards', model='sprint') |
    models.Q(app_label='boards', model='sticker')
)


@receiver(post_save, sender=Profile)
def new_profile_handler(sender, instance, **kwargs):
    """
    Catch post_save signal of `Profile` model to create a `Desk` for new user.
    """
    if not Desk.objects.filter(owner=instance).exists():
        Desk.objects.create(
            owner=instance, desk_slug=instance.user.username[-5:]
        )


class DeskBoardMixin(models.Model):
    """
    Common methods and attributes od Desk and Board models.
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


class CommentInfoMixin(models.Model):
    """
    Common methods and attributes of Board and Sticker models.
    @desc: model mixin.
    """
    # @desc: example of property.
    @property
    def count_comments(self):
        """
        Return number of comment of a sticker.
        """
        content_type = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(
            content_type=content_type, object_id=self.pk
        ).count()

    class Meta:
        abstract = True


class CommonInfoMixin(models.Model):
    """
    Abstract class for models' common information.
    @desc: abstract model class.
    """
    # @desc: foreign key to different app.
    author = models.ForeignKey('profiles.Profile', verbose_name=_('author'))
    # @desc: using of auto_now_add.
    creation_date = models.DateTimeField(
        _('creation date'), auto_now_add=True, editable=False
    )
    # @desc: using of auto_now.
    modification_date = models.DateTimeField(
        _('creation date'), auto_now=True, editable=False
    )

    class Meta:
        abstract = True


class Comment(CommonInfoMixin):
    """
    There is a possibility to comment Stickers or Boards. This model store
    all comments.
    """
    # @desc: generic relation.
    text = models.TextField(_('text'))
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(
        ContentType, limit_choices_to=COMMENT_LOCATION_LIMIT
    )
    object_id = models.PositiveIntegerField()

    objects = models.Manager()
    authors_objects = CommentAuthorsManager()

    def __str__(self):
        return '@{} [{}]'.format(self.author, self.creation_date)


class Label(models.Model):
    """
    Represents status of task for particular `Sticker` object.
    """
    # @desc: custom field.
    color = RGBField(_('color'))
    css_class = models.CharField(
        _('css class'), choices=CSS_CLASS, max_length=100
    )
    status = models.CharField(_('status'), choices=TASK_STATUS, max_length=1)

    def __str__(self):
        return '{}'.format(self.status, self.color)


class Desk(DeskBoardMixin, models.Model):
    """
    Boards container model.
    """
    # @desc: OneToOne relation.
    owner = models.OneToOneField('profiles.Profile', verbose_name=_('owner'))
    desk_slug = models.SlugField(max_length=5, unique=True)

    def __str__(self):
        return self.desk_slug

    @property
    def boards(self):
        """
        Returns boards of particular desk.
        """
        return self.owner.board_set.all()


class Board(CommentInfoMixin, DeskBoardMixin, CommonInfoMixin):
    """
    Stickers container model.
    """
    desk = models.ForeignKey(Desk, verbose_name=_('desk'))
    title = models.CharField(_('title'), max_length=100)
    sequence = models.PositiveIntegerField(_('sequence'))
    prefix = models.SlugField(_('prefix'), max_length=5)
    sticker_sequence = models.PositiveIntegerField(
        _('sticker sequence'), default=1
    )

    def __str__(self):
        return '{} [{}]'.format(self.title, self.desk)

    @property
    def get_next_sequence(self):
        """
        Return next board sequence
        """
        last_sequence = Board.objects.filter(desk=self.desk).aggregate(
            models.Max('sequence')
        ).get('sequence__max') or 0
        return last_sequence + 1

    @property
    def owner_username(self):
        """
        Return owner's username of board, so owner of desk that this board
        is assigned to (not author of board).
        """
        return self.desk.owner.user.username

    def save(self, *args, **kwargs):
        """
        Populate prefix if has not been provided.
        """
        if not self.prefix:
            self.prefix = self.desk.desk_slug

        if not self.pk:
            self.sequence = self.get_next_sequence
        super(Board, self).save(*args, **kwargs)

    class Meta:
        # @desc: unique constrains.
        unique_together = ('desk', 'sequence')


class Sprint(CommentInfoMixin, CommonInfoMixin):
    """
    Sprint for creating next phases of learning.
    """
    board = models.ForeignKey(Board, verbose_name=_('board'))
    number = models.DecimalField(_('number'), decimal_places=2, max_digits=5)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))

    def __str__(self):
        return 'SPRINT#{}/BOARD#{} [{}]'.format(
            self.number, self.board.sequence, self.board.desk.owner
        )

    @property
    def time_to_finish(self):
        """
        Return time that left to the end of a sprint.
        """
        return self.end_date - datetime.now()

    @property
    def is_current(self):
        """
        Return if sprint is in progress.
        """
        return self.end_date < datetime.now()

    class Meta:
        unique_together = ('board', 'number')


class Sticker(CommentInfoMixin, CommonInfoMixin):
    """
    Sticker with task description.
    """
    board = models.ForeignKey(Board, verbose_name=_('board'))
    caption = models.CharField(_('caption'), max_length=100)
    # @desc: long text field.
    description = models.TextField(_('description'))
    label = models.ForeignKey(Label, verbose_name=_('label'))
    sequence = models.PositiveIntegerField(_('sequence'))
    # @desc: choices field.
    sprint = models.ForeignKey(
        Sprint, blank=True, null=True, verbose_name=_('sprint')
    )
    # status = models.CharField(_('status'), choices=TASK_STATUS, max_length=1)

    objects = StickersManager()

    def __str__(self):
        return '#{}-{} {} [{}]'.format(
            self.board.prefix, self.sequence, self.caption, self.label.status
        )

    @property
    def css_class(self):
        """
        Return css class name basing on a sticker's status.
        """
        return '{}-{}'.format(self.board.prefix, self.sequence)

    @property
    def number(self):
        """
        Return number of ticket
        """
        return '{}-{}'.format(self.board.prefix, self.sequence)

    def save(self, *args, **kwargs):
        """
        Populate and update sequence.
        """
        if not self.pk:
            sequence = self.board.sticker_sequence
            self.sequence = sequence
            self.board.sticker_sequence = sequence + 1
            self.board.save()
        super(Sticker, self).save(*args, **kwargs)

    class Meta:
        # @desc: unique constrains.
        unique_together = ('board', 'sequence')
