from django import forms


class SitemapForm(forms.Form):
    slug = forms.SlugField(required=False)
