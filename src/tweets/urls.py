from django.conf.urls import url
from .views import TweetDetailView, TweetListView


urlpatterns = [
    url(r'^$', TweetListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'),
]