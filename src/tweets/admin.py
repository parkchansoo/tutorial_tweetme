from django.contrib import admin
from .models import Tweet
from .forms import TweetModelForm




class TweetModelFormAdmin(admin.ModelAdmin):

    form = TweetModelForm
    # class Meta:
    #     model = Tweet
    #     form = TweetModelForm


admin.site.register(Tweet, TweetModelFormAdmin)