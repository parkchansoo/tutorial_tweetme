from django.contrib import admin
from .models import Tweet
from .forms import TweetModelForm




class TweetModelFormAdmin(admin.ModelAdmin):
    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetModelFormAdmin)