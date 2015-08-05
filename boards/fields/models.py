# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import CharField
from django.core.validators import RegexValidator

from boards.fields import forms


class RGBField(CharField):
    """
    Custom field for color values in RGB model.

    @desc: custom model field.
    """
    default_validators = [RegexValidator(regex=forms.RGB_REGEX)]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(RGBField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RGBField}
        defaults.update(kwargs)
        return super(RGBField, self).formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(RGBField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
