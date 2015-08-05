# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import RegexField

from boards.validators import RGB_REGEX


class RGBField(RegexField):
    """
    RGB form field.

    @desc: custom form field.
    """
    def __init__(self, **kwargs):
        kwargs['regex'] = RGB_REGEX
        super(RGBField, self).__init__(**kwargs)
