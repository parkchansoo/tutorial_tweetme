from django.shortcuts import render
from .models import Tweet


def tweet_detail_view(request, id=1):
    obj = Tweet.objects.get(id=id)
    print(obj)
    context = {
        "object": obj,
        "abc": obj
    }
    return render(request, "tweets/detail_view.html", context)

def tweet_list_view(request):
    queryset = Tweet.objects.all()
    for obj in queryset:
        print(obj)
    context = {
        "object_list": queryset
    }
    return render(request, "tweets/list_view.html", context)