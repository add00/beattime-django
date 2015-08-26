# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from profiles.models import Profile


class ProfileUpdateForm(ModelForm):
    """
    Model form for `Profile` model for update purposes.
    """

    def __init__(self, *args, **kwargs):
        """
        Provide profile object to form for clean purposes.
        Avoid 'self frending'.
        """
        self.profile = kwargs.pop('profile')
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        if self.profile:
            self.fields['friends'].queryset = (
                Profile.objects.exclude(pk=self.profile.pk)
            )

    def clean_avatar(self):
        """
        Change avatar name to profile's username.
        """
        avatar = self.cleaned_data['avatar']
        if avatar:
            _, extension = os.path.splitext(avatar.name)
            avatar.name = '{}{}'.format(
                self.profile.user.username, extension
            )

        return avatar

    class Meta:
        model = Profile
        fields = ['display_name', 'friends', 'motivation_quote', 'avatar']


class ProfileCreationForm(UserCreationForm):
    """
    New profile form
    """
    avatar = forms.ImageField(required=False)
    display_name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True)
    motivation_quote = forms.CharField(max_length=255, required=False)
    username = forms.CharField(max_length=254)

    def save(self, commit=True):
        user = super(ProfileCreationForm, self).save(commit=True)
        data = self.cleaned_data
        Profile.objects.create(
            avatar=data['avatar'],
            display_name=data['display_name'],
            motivation_quote=data['motivation_quote'],
            user=user
        )
        return user

    class Meta(UserCreationForm.Meta):
        fields = [
            'username', 'password1', 'password2', 'email', 'display_name',
            'motivation_quote', 'avatar'
        ]
