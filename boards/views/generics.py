# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import generic

from boards.models import Board


class BoardsBoardView(generic.ListView):
    model = Board
    template_name = 'boards/board.html'


class BoardsProfileView(generic.TemplateView):
    template_name = 'boards/profile.html'
