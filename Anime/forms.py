from django import forms

class SearchForm(forms.Form):
    anime_title = forms.CharField()
    source = forms.CharField()