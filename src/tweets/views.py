from django import forms
from django.forms.utils import ErrorList
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Tweet

from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin

from django.db.models import Q


class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            if new_tweet:
                return HttpResponseRedirect(new_tweet.get_absolute_url())
            else:
                pass
        return HttpResponseRedirect(tweet.get_absolute_url())


class TweetCreateView(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'


class TweetDeleteView(DeleteView):
    model = Tweet
    template_name = "tweets/delete_view.html"
    # success_url = reverse("tweets:list")


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

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all()
        query = self.request.GET.get("q", None)
        print(query)
        print(self.request.GET)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        # context["another_list"] = Tweet.objects.all()
        # print(context)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy("tweets:create")
        return context
