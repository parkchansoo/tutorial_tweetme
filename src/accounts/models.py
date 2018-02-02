from django.db import models
from django.conf import settings


class userProfileManager(models.Manager):
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

class UserProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    # with query > html gets specific user as objects > objects.profile gives own userProfile model > profile.following give user who i follow
    following   = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    # with query > html gets specific user as objects > objects.folled_by gives UserProfile who follows me!

    objects = userProfileManager()  # UserProfile.objects.all()
    # abc     = userProfileManager()  # UserProfile.abc.all()


    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)