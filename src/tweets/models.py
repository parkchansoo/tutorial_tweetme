import re

from django.urls import reverse
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

from .validators import validate_content
from hashtags.signals import parsed_hashtags

# def validate_content(value):
#     content = value
#     if content == 'abc':
#         raise ValidationError("Content cannot be ABC")
#     return value

class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        print(type(parent_obj[0]))

        if parent_obj[0].parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj[0]

        qs = self.get_queryset().filter(user=user, parent=og_parent)
        if qs.exists():
            return None

        obj = self.model(
            parent  =og_parent,
            user    =user,
            content =og_parent.content,
        )
        obj.save()
        print(obj.parent.id)
        return obj

    def like_toggle(self, user, tweet_obj):
        print(type(tweet_obj))
        print(user)
        if user in tweet_obj.liked.all():
            print('user is in liked model')
            is_liked = False
            tweet_obj.liked.remove(user)
            print(tweet_obj.liked.count())
        else:
            print('user isnt on liked model')
            is_liked = True
            tweet_obj.liked.add(user)
            print(tweet_obj.liked.count())
        print(is_liked)
        return is_liked


class Tweet(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.CharField(max_length=140, default="tweet anyting", validators=[validate_content])
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    updated_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.BooleanField(verbose_name='is a reply', default=False)

    objects = TweetManager()

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("tweets:detail", kwargs={'pk':self.pk})

    # def clean(self, *args, **kwargs):
    #     content = self.content
    #     if content == 'abc':
    #         raise ValidationError("Content cannnot be abc")
    #     return super(Tweet, self).clean(*args, **kwargs)\


def tweet_save_receiver(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)

        # if m:
        #     username = m.group("username")
        #     print(username)
        #     #send notification to user here.

        hash_regex = r'#(?P<hashtag>[\w.@+-]+)'
        hashtags = re.findall(hash_regex, instance.content)
        print(hashtags)
        # send notification to user here.
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)


post_save.connect(tweet_save_receiver, sender=Tweet)