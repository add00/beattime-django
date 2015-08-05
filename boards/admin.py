from django.contrib import admin

from boards import models


class StickerInline(admin.StackedInline):
    model = models.Sticker
    extra = 1


class BoardAdmin(admin.ModelAdmin):
    inlines = [StickerInline]

admin.site.register(models.Board, BoardAdmin)
