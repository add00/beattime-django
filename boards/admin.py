from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from boards.models import Board, Comment, Desk, Label, Sticker


class StickerInline(admin.StackedInline):
    model = Sticker
    extra = 1


class BoardInline(admin.StackedInline):
    model = Board
    extra = 1


class CommentInline(GenericStackedInline):
    model = Comment
    extra = 1


class BoardAdmin(admin.ModelAdmin):
    inlines = [StickerInline, CommentInline]


class DeskAdmin(admin.ModelAdmin):
    inlines = [BoardInline]


class StickerAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


admin.site.register(Board, BoardAdmin)
admin.site.register(Desk, DeskAdmin)
admin.site.register(Label)
admin.site.register(Sticker, StickerAdmin)
