# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.http import JsonResponse

from boards.models import Sticker


class StickerAPI(View):

    def get(self, request):
        """
        Return stickers for logged in user.
        """
        stickers = {
            sticker.number: {
                'status': sticker.label.status,
                'caption': sticker.caption,
                'description': sticker.description,
            }
            for sticker in Sticker.objects.filter(
                board__desk__owner__user=request.user
            )
        }
        return JsonResponse(stickers)
