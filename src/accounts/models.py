from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models.signals import post_save, pre_save


class UserProfileManager(models.Manager):
    use_for_related_field = True
    def all(self):
        qs = self.get_queryset().all()
        print(qs)
        print(self.instance)
        try:
            if(self.instance):
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = self.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False


class UserProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    # with query > html gets specific user as objects > objects.profile gives own userProfile model > profile.following give user who i follow
    following   = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    # with query > html gets specific user as objects > objects.folled_by gives UserProfile who follows me!

    objects = UserProfileManager()  # UserProfile.objects.all()
    # abc     = userProfileManager()  # UserProfile.abc.all()


    def __str__(self):
        return "{}, {}".format(self.user.username, self.following.all().count())

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)

    def get_following_url(self):
        return reverse_lazy("profiles:follow", kwargs={'username':self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("profile:detail", kwargs={'username':self.user.username})


# chansoo = User.object.first
# chansoo.save()



def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)
        # celery + redis
        # deferred task

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)