# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import ModelForm

from boards.models import Comment


class CommentForm(ModelForm):
    """
    Model form for `Comment` model.
    """

    def __init__(self, *args, **kwargs):
        """
        Change `text` field's widget CSS class.
        """
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['rows'] = 3
        self.fields['text'].label = ''

    class Meta:
        model = Comment
        fields = ['text']
