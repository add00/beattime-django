from django.contrib import admin

from boards.models import Board, Desk, Label, Sticker


class StickerInline(admin.StackedInline):
    model = Sticker
    extra = 1


class BoardInline(admin.StackedInline):
    model = Board
    extra = 1


class BoardAdmin(admin.ModelAdmin):
    inlines = [StickerInline]


class DeskAdmin(admin.ModelAdmin):
    inlines = [BoardInline]


admin.site.register(Board, BoardAdmin)
admin.site.register(Desk, DeskAdmin)
admin.site.register(Label)
admin.site.register(Sticker)
