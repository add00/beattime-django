from django.db.models import Count, Manager, QuerySet

from boards import OPEN, IN_PROGRESS, IN_REVIEW, DONE, BLOCKED


class CommentAuthorsManager(Manager):
    """
    Custom manager overridding queryset to return authors of comments,
    ordering by activity (whole number of comments).
    """

    def get_queryset(self):
        return super(CommentAuthorsManager, self).get_queryset().values(
            'author'
        ).annotate(author_times=Count('author')).order_by('-author_times')


class StickersQuerySet(QuerySet):
    """
    Custom queryset to get simple access to stickers with particular state.
    """
    def open(self):
        return self.filter(label__status=OPEN)

    def in_progress(self):
        return self.filter(label__status=IN_PROGRESS)

    def review(self):
        return self.filter(label__status=IN_REVIEW)

    def done(self):
        return self.filter(label__status=DONE)

    def blocked(self):
        return self.filter(label__status=BLOCKED)


class StickersManager(Manager):
    """
    Custom manager to get quick access to stickers with different statuses.
    """
    def get_queryset(self):
        return StickersQuerySet(self.model, using=self._db)

    def open(self):
        return self.get_queryset().open()

    def in_progress(self):
        return self.get_queryset().in_progress()

    def review(self):
        return self.get_queryset().review()

    def done(self):
        return self.get_queryset().done()

    def blocked(self):
        return self.get_queryset().blocked()
