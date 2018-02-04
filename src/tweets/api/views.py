from rest_framework import generics
from rest_framework import permissions
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TweetModelSerializer
from tweets.models import Tweet
from .pagination import StandardResultsPagination


class RetweetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = "not allowed"
        if tweet_qs.exists() and tweet_qs.count() == 1:
            # if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user, tweet_qs)
            message = "already exists"
            if new_tweet is not None:
                data = TweetModelSerializer(tweet_qs.first()).data
                return Response(data)
        return Response({"message":message}, status=400)


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer(user=self.request.user)


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    # permission_classes =
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        im_following = self.request.user.profile.get_following()
        query = self.request.GET.get("q", None)
        qs1 = Tweet.objects.filter(user__in=im_following)
        qs2 = Tweet.objects.filter(user=self.request.user)
        qs = (qs1 | qs2).distinct().order_by("-timestamp")
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs