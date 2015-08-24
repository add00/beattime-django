# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.widgets import HiddenInput
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from boards import DETAIL, CREATE, LIST, OPEN, UPDATE
from boards.forms import CommentForm
from boards.mixins import (
    BoardMixin, ContextMixin, CommentsMixin, CommonInfoMixin, SprintMixin,
    StickerMixin,
)
from boards.models import Board, Comment, Desk, Label, Sprint, Sticker
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
        elif self.url_name == 'board-comments':
            return Board.objects.get(
                desk__owner__user=self.user,
                sequence=self.kwargs['board_sequence']
            )
        elif self.url_name == 'sprint-comments':
            return Sprint.objects.get(
                number=self.kwargs['sprint_number'],
                board__desk__owner__user=self.user,
                board__sequence=self.kwargs['board_sequence']
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
        context['sprints'] = Sprint.objects.filter(board=self.object)
        return context

    def get_queryset(self):
        """
        Return queryset of stickers that belong to desk
        of user sending a request.
        """
        self.object = self.get_object()
        return self.object.sticker_set.filter(sprint__isnull=True).order_by(
            '-modification_date'
        )


class BoardCreate(BoardMixin, CreateView):
    action = CREATE

    def form_valid(self, form):
        """
        Specify desk and author.
        """
        author = Profile.objects.get(user=self.request.user)
        desk = Desk.objects.get(owner__user=self.user)
        form.instance.author = author
        form.instance.desk = desk

        return super(BoardCreate, self).form_valid(form)


class BoardComments(CommentsMixin, BoardMixin, ListView):
    action = LIST

    def post(self, request, *args, **kwargs):
        """
        Handle comment.
        """
        view = CommentCreate.as_view()
        return view(request, *args, **kwargs)


class SprintDetail(SprintMixin, ListView):
    action = DETAIL
    template_name = 'boards/sprint.html'

    def get_context_data(self, **kwargs):
        """
        Append set of sprint's stickers.
        """
        context = super(SprintDetail, self).get_context_data(**kwargs)
        context['stickers'] = self.get_queryset()
        return context

    def get_queryset(self):
        """
        Return stickers for particular sprint of
        """
        self.object = self.get_object()
        return self.object.sticker_set.all().order_by('-modification_date')


class SprintCreate(SprintMixin, CreateView):
    action = CREATE

    def get_form_kwargs(self):
        """
        Append extra kwargs to form for validation purposes.
        """
        kwargs = super(SprintCreate, self).get_form_kwargs()
        self.board = Board.objects.get(
            desk__owner__user=self.user,
            sequence=self.kwargs['board_sequence']
        )
        extra_kwargs = {'board': self.board}
        kwargs.update(extra_kwargs)
        return kwargs

    def form_valid(self, form):
        """
        Specify board and author.
        """
        author = Profile.objects.get(user=self.request.user)
        form.instance.author = author
        form.instance.board = self.board

        return super(SprintCreate, self).form_valid(form)


class SprintComments(CommentsMixin, SprintMixin, ListView):
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
    action = CREATE

    def get_form(self):
        """
        Disable `label` field (default OPEN while creating new).
        Handle cases with adding new sticker both to board and sprint.
        """
        form = super(StickerCreate, self).get_form()

        form.fields.pop('label')

        if self.kwargs.get('sprint_number'):
            board = Board.objects.get(
                desk__owner__user=self.user,
                sequence=self.kwargs['board_sequence']
            )
            form.initial = {
                'sprint': Sprint.objects.get(
                    number=self.kwargs['sprint_number'], board=board
                )
            }
            form.fields['sprint'].widget = HiddenInput()
        else:
            form.fields['sprint'].empty_label = 'Backlog'

        return form

    def form_valid(self, form):
        """
        Append default data while creating a sticker, not provided in a form.
        """
        author = Profile.objects.get(user=self.request.user)
        board = Board.objects.get(
            desk__owner__user=self.user,
            sequence=self.kwargs['board_sequence']
        )
        label = Label.objects.get(status=OPEN)
        form.instance.author = author
        form.instance.board = board
        form.instance.label = label

        return super(StickerCreate, self).form_valid(form)


class StickerUpdate(StickerMixin, UpdateView):
    action = UPDATE
