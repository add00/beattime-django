# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import ModelForm

from boards.models import Sticker


class StickerForm(ModelForm):
    """
    Model form for `Sticker` model.
    """

    class Meta:
        model = Sticker
        fields = ['caption', 'description', 'label']
