from django.db import models
from django.urls import reverse_lazy

from tweets.models import Tweet

class HashTag(models.Model):
    tag = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse_lazy("hashtag", kwargs={"hashtag":self.tag})

    def get_tweets(self):
        tweet_set = Tweet.objects.filter(content__icontains="#" + self.tag)
        print("print...")
        print(tweet_set)
        return tweet_set