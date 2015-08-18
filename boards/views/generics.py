# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from boards import DETAIL, LIST, OPEN, UPDATE
from boards.forms import CommentForm
from boards.mixins import (
    BoardMixin, CommentsMixin, CommonInfoMixin, StickerMixin, ContextMixin
)
from boards.models import Board, Comment, Sticker
from profiles.models import Profile


class CommentCreate(CommonInfoMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_object(self):
        """
        Return sticker or board, basing on request.
        """
        if not self.user.is_authenticated():
            raise Http404('Access denied')
        self.url_name = self.request.resolver_match.url_name
        if self.url_name == 'sticker-detail':
            return Sticker.objects.get(
                board__desk__owner__user=self.user,
                board__prefix=self.kwargs['prefix'],
                sequence=self.kwargs['sequence']
            )
        return Board.objects.get(
            desk__owner__user=self.user,
            sequence=self.kwargs['board_sequence']
        )

    def get_success_url(self):
        """
        After creation, back to a previous page.
        """
        kwargs = {
            key: value for key, value in self.kwargs.iteritems() if value
        }
        return reverse('boards:{}'.format(self.url_name), kwargs=kwargs)

    def form_valid(self, form):
        """
        Append default data while creating a comment, not provided in a form.
        """
        author = Profile.objects.get(user=self.request.user)
        object = self.get_object()
        content_type = ContentType.objects.get_for_model(object)
        form.instance.author = author
        form.instance.content_type = content_type
        form.instance.object_id = object.pk

        return super(CommentCreate, self).form_valid(form)


class ProfileDetail(ContextMixin, ListView):
    action = DETAIL
    template_name = 'boards/profile.html'
    context_object_name = 'boards'

    def get_queryset(self):
        """
        Return only boards from desk of user that sent a request.
        """
        if self.user.is_authenticated():
            return Board.objects.filter(desk__owner__user=self.user)


class BoardDetail(BoardMixin, ListView):
    action = DETAIL

    def get_context_data(self, **kwargs):
        """
        Append set of board's stickers.
        """
        context = super(BoardDetail, self).get_context_data(**kwargs)
        context['stickers'] = self.get_queryset()
        return context

    def get_queryset(self):
        """
        Return queryset of stickers that belong to desk
        of user sending a request.
        """
        self.object = self.get_object()
        return self.object.sticker_set.all()


class BoardComments(CommentsMixin, BoardMixin, ListView):
    action = LIST

    def post(self, request, *args, **kwargs):
        """
        Handle comment.
        """
        view = CommentCreate.as_view()
        return view(request, *args, **kwargs)


class StickerDetail(CommentsMixin, StickerMixin, ListView):
    action = DETAIL

    def post(self, request, *args, **kwargs):
        """
        Handle comment.
        """
        view = CommentCreate.as_view()
        return view(request, *args, **kwargs)


class StickerCreate(StickerMixin, CreateView):

    def form_valid(self, form):
        """
        Append default data while creating a sticker, not provided in a form.
        """
        author = Profile.objects.get(user=self.request.user)
        board = Board.objects.get(
            desk__owner__user=self.user,
            sequence=self.kwargs['board_sequence']
        )
        form.instance.author = author
        form.instance.board = board
        form.instance.status = OPEN[0]

        return super(StickerCreate, self).form_valid(form)


class StickerUpdate(StickerMixin, UpdateView):
    action = UPDATE
