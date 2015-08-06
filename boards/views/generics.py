# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.views import generic

from boards.models import Board, Sticker


class BoardView(generic.ListView):
    template_name = 'boards/board.html'
    context_object_name = 'stickers'

    def get_queryset(self):
        """
        Return queryset of stickers that belong to desk
        of user sending a request.
        """
        return Sticker.objects.filter(
            board__desk__owner__user__username=self.kwargs['username'],
            board__sequence=self.kwargs['board_sequence']
        )


class ProfileView(generic.ListView):
    template_name = 'boards/profile.html'
    context_object_name = 'boards'

    def get_queryset(self):
        """
        Return only boards from desk of user that sent a request.
        """
        user = self.request.user
        if user.is_authenticated():
            return Board.objects.filter(desk__owner__user=user)
