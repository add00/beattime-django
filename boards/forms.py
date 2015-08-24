# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.forms import ModelForm, ValidationError

from boards.models import Comment, Sprint


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


class SprintForm(ModelForm):
    """
    Model form for `Sprint` model.
    """

    def __init__(self, *args, **kwargs):
        """
        Change `text` field's widget CSS class.
        """
        self.board = kwargs.pop('board')
        super(SprintForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs = {'class': 'datepicker'}
        self.fields['end_date'].widget.attrs = {'class': 'datepicker'}

    def _is_past_date(self, date, field_name):
        """
        Check if date is a past date.
        """
        if date and date < datetime.now().date():
            self.add_error(
                field_name,
                '{} is a past date'.format(
                    field_name.title().replace('_', ' ')
                )
            )

    def clean(self):
        """
        Past dates are not allowed.
        `start_date` must be earlier date than `end_date`
        """
        cleaned_data = super(SprintForm, self).clean()
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']

        if start_date:
            if end_date < start_date:
                self.add_error(
                    None,
                    'End date is earlier date than Start date'
                )
        self._is_past_date(start_date, 'start_date')
        self._is_past_date(end_date, 'end_date')

        return cleaned_data

    def clean_number(self):
        """
        Unique sprint number (in particular board) constrain.
        """
        number = self.cleaned_data['number']
        if Sprint.objects.filter(
            board=self.board, number=number
        ).exists():
            raise ValidationError(
                'Sprint with {} number already exists'.format(
                    number
                )
            )

        return number

    class Meta:
        model = Sprint
        fields = ['number', 'start_date', 'end_date']
