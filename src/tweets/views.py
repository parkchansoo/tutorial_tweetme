from django import forms
from django.forms.utils import ErrorList

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import Tweet

from  .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin


class TweetCreateView(FormUserNeededMixin, CreateView):
    # queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    success_url = '/tweets/create'
    # login_url = '/admin/login/'


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    success_url = "/tweets/"


'''
we don't have to give template name class based view
because we only type html file like "(model_name)_(viewname).html" than it's ok
'''


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()

    # def get_object(self):
    #     print(self.kwargs)
    #     pk = self.kwargs.get('pk')
    #     # obj = Tweet.objects.get(id=pk)
    #     obj = get_object_or_404(Tweet, pk=pk)
    #     return obj


class TweetListView(ListView):
    queryset = Tweet.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        # context["another_list"] = Tweet.objects.all()
        # print(context)
        return context


# def tweet_detail_view(request, id=1):
#     obj = Tweet.objects.get(id=id)
#     print(obj)
#     context = {
#         "object": obj,
#         "abc": obj
#     }
#     return render(request, "tweets/detail_view.html", context)
#
# def tweet_list_view(request):
#     queryset = Tweet.objects.all()
#     for obj in queryset:
#         print(obj)
#     context = {
#         "object_list": queryset
#     }
#     return render(request, "tweets/list_view.html", context)
