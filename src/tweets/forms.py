from django import forms
from .models import Tweet


class TweetModelForm(forms.ModelForm):
    # title = forms.CharField(required=False)
    # content = forms.CharField(label='',
    #                           widget=forms.Textarea(
    #                               attrs={'placeholder': "Your message", "class": "form-control"})
    #                           ),
    class Meta:
        model = Tweet
        fields = [
            # "user",
            "content",
        ]

    # def clean_content(self, *args, **kwargs): #clean_(field_name)
    #     content = self.cleaned_data.get("content")
    #     if content == "abc":
    #         raise forms.ValidationError("Cannot be abc")
    #     return
