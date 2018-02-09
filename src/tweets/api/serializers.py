from django.utils.timesince import timesince
from rest_framework import serializers

from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer


class ParentTweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer()
    date_dsiplay = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'user',
            'content',
            'timestamp',
            'date_dsiplay',
            'timesince',
        ]

    def get_date_dsiplay(self, obj):
        return obj.timestamp.strftime("%b %d %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class TweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer()
    date_dsiplay = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    parent = ParentTweetModelSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'pk',
            'user',
            'content',
            'timestamp',
            'date_dsiplay',
            'timesince',
            'parent',
            'like_count',
            'did_like',
            'reply'
        ]
    def get_did_like(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated():
            if user in obj.liked.all():
                return True
        return False

    def get_date_dsiplay(self, obj):
        return obj.timestamp.strftime("%b %d %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_like_count(self, obj):
        return obj.liked.all().count()