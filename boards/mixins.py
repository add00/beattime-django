# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from boards.forms import CommentForm
from boards.models import Board, Comment, Sticker
from boards.utils import get_user


class CommonInfoMixin(object):
    """
    Append common data to view instace.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Overridde `dispatch` method to provide extra variables.
        """
        # @desc: extra view instance variable using request.
        self.user = get_user(request, self.kwargs)
        return super(CommonInfoMixin, self).dispatch(request, *args, **kwargs)


class ContextMixin(CommonInfoMixin):
    """
    Mixin class to pass kwargs and other extra data to context.
    """
    action = None

    # @desc: private method.
    def _get_short_urls_allowed(self):
        """
        Return if `username` argument can be omitted while rendering urls.
        """
        return self.kwargs.get('username') is None

    def get_context_data(self, **kwargs):
        """
        Update context data on request keyword arguments to have a simple
        access to view data, for instace url parameters.
        Add `short_urls_allowed` variable indicating if a displayed element
        (e.g. profile, board, sticker) is owned by logged user so username
        can be omitted.
        Also append action to context data to know action of page.
        """
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['action'] = self.action
        context['short_urls_allowed'] = self._get_short_urls_allowed()
        context['username'] = get_user(self.request, self.kwargs).username
        kwargs = {
            key: value for key, value in self.kwargs.iteritems()
            if key not in context
        }
        context.update(**kwargs)

        return context


class BoardMixin(ContextMixin, SingleObjectMixin):
    """
    Mixin class for Board model.
    """
    content_type = ContentType.objects.get_for_model(Board)
    template_name = 'boards/board.html'

    def get_object(self):
        """
        Return board basing od kwargs.
        """
        if not self.user.is_authenticated():
            # Redirect to log in page.
            raise Http404('Access denied')

        return Board.objects.get(
            desk__owner__user=self.user,
            sequence=self.kwargs['board_sequence']
        )


class StickerMixin(ContextMixin, SingleObjectMixin):
    """
    Mixin class for Sticker model.
    """
    content_type = ContentType.objects.get_for_model(Sticker)
    context_object_name = 'sticker'
    fields = ['caption', 'description', 'label']
    model = Sticker
    template_name = 'boards/sticker.html'

    def get_success_url(self):
        """
        After creation or update, back to a sticker preview.
        """
        kwargs = {
            key: value for key, value in self.kwargs.iteritems() if value
        }
        return reverse(
            'boards:sticker-detail', kwargs=kwargs
        )

    def get_object(self):
        """
        Return sticker for given number from requesting user's board.
        Sticker can be editted by its author or owner of desk.
        """
        if not self.user.is_authenticated():
            # Redirect to log in page.
            raise Http404('Access denied')

        return Sticker.objects.get(
            board__desk__owner__user=self.user,
            board__prefix=self.kwargs['prefix'],
            sequence=self.kwargs['sequence']
        )


class CommentsMixin(MultipleObjectMixin):
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        """
        Set view's object instance.
        """
        self.object = self.get_object()
        return super(CommentsMixin, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filter comments to list of sticker or board's ones.
        """
        return Comment.objects.filter(
            content_type=self.content_type, object_id=self.object.pk
        ).order_by('-creation_date')

    def get_context_data(self, **kwargs):
        """
        Provide comments list and comment form to context data.
        """
        context = super(CommentsMixin, self).get_context_data(**kwargs)
        context['comments'] = self.get_queryset()
        context['comment_form'] = CommentForm
        return context
