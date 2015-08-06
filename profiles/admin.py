from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from profiles.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1


class ProfileUserAdmin(UserAdmin):
    inlines = [ProfileInline]

    # @desc: self and a ManyToMany relation.
    def save_model(self, request, obj, form, change):
        """
        If user has no related `Profile` object then create one.
        """
        obj.save()
        Profile.objects.get_or_create(user=obj)

admin.site.unregister(User)
admin.site.register(User, ProfileUserAdmin)
