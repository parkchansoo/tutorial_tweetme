from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from .validators import validate_content

# def validate_content(value):
#     content = value
#     if content == 'abc':
#         raise ValidationError("Content cannot be ABC")
#     return value


class Tweet(models.Model):
    # user
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content     = models.CharField(max_length=140, default="tweet anyting", validators=[validate_content])
    updated_at  = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)

    # def clean(self, *args, **kwargs):
    #     content = self.content
    #     if content == 'abc':
    #         raise ValidationError("Content cannnot be abc")
    #     return super(Tweet, self).clean(*args, **kwargs)