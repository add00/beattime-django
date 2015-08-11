# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import Http404

from boards.models import Sticker
from boards.utils import get_user


class CommonInfoMixin(object):
    """
    Append common data to view instace.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Overridde `dispatch` method to provide extra variables.
        """
        # @desc: extra view instance variable using request.
        self.user = get_user(request, self.kwargs)
        return super(CommonInfoMixin, self).dispatch(request, *args, **kwargs)


class ContextMixin(CommonInfoMixin):
    """
    Mixin class to pass kwargs and other extra data to context.
    """
    action = None

    # @desc: private method.
    def _get_short_urls_allowed(self):
        """
        Return if `username` argument can be omitted while rendering urls.
        """
        return self.kwargs.get('username') is None

    def get_context_data(self, **kwargs):
        """
        Update context data on request keyword arguments to have a simple
        access to view data, for instace url parameters.
        Add `short_urls_allowed` variable indicating if a displayed element
        (e.g. profile, board, sticker) is owned by logged user so username
        can be omitted.
        Also append action to context data to know action of page.
        """
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context['action'] = self.action
        context['short_urls_allowed'] = self._get_short_urls_allowed()
        context['username'] = get_user(self.request, self.kwargs).username
        kwargs = {
            key: value for key, value in self.kwargs.iteritems()
            if key not in context
        }
        context.update(**kwargs)

        return context


class StickerMixin(ContextMixin):
    """
    Mixin class for Sticker model.
    """
    context_object_name = 'sticker'
    fields = ['caption', 'description', 'label']
    model = Sticker
    template_name = 'boards/sticker.html'

    def get_success_url(self):
        """
        After creation or update, back to a sticker preview.
        """
        kwargs = {
            key: value for key, value in self.kwargs.iteritems() if value
        }
        return reverse(
            'boards-sticker-detail', kwargs=kwargs
        )

    def get_object(self):
        """
        Return sticker for given number from requesting user's board.
        Sticker can be editted by its author or owner of desk.
        """
        if not self.user.is_authenticated():
            # Redirect to log in page.
            raise Http404('Access denied')

        return Sticker.objects.get(
            board__desk__owner__user=self.user,
            board__prefix=self.kwargs['prefix'],
            sequence=self.kwargs['sequence']
        )
