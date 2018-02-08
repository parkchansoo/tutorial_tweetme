import re

from django.urls import reverse
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

from .validators import validate_content

# def validate_content(value):
#     content = value
#     if content == 'abc':
#         raise ValidationError("Content cannot be ABC")
#     return value

class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

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


class Tweet(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content = models.CharField(max_length=140, default="tweet anyting", validators=[validate_content])
    updated_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

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
        # if h_m:
        #     hashtag = m.group("hashtag")
        #     print(hashtag)
        #     # send hashtag signal to user


post_save.connect(tweet_save_receiver, sender=Tweet)