from django import forms


class SitemapForm(forms.Form):
    slug = forms.SlugField(required=False)


class SearchForm(forms.Form):
    searchstring = forms.CharField(help_text="What are you looking for?")
