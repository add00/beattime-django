# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from boards import DETAIL, OPEN, UPDATE
from boards.mixins import StickerMixin, ContextMixin
from boards.models import Board, Sticker
from profiles.models import Profile


class BoardView(ContextMixin, ListView):
    template_name = 'boards/board.html'
    context_object_name = 'stickers'

    def get_queryset(self):
        """
        Return queryset of stickers that belong to desk
        of user sending a request.
        """
        return Sticker.objects.filter(
            board__desk__owner__user=self.user,
            board__sequence=self.kwargs['board_sequence']
        )


class ProfileView(ContextMixin, ListView):
    template_name = 'boards/profile.html'
    context_object_name = 'boards'

    def get_queryset(self):
        """
        Return only boards from desk of user that sent a request.
        """
        if self.user.is_authenticated():
            return Board.objects.filter(desk__owner__user=self.user)


class StickerDetail(StickerMixin, DetailView):
    action = DETAIL


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
