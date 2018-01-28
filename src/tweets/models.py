from django.db import models
from django.conf import settings


class Tweet(models.Model):
    # user
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content     = models.CharField(max_length=140, default="tweet anyting")
    updated_at  = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)