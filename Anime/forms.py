from django import forms

class SearchForm(forms.Form):
    anime_title = forms.CharField()
    
class Sign_upForm(forms.Form):
    name = forms.CharField()
    gender = forms.CharField()
    birthdate = forms.DateField()
    location = forms.CharField()
    
class log_inForm(forms.Form):
    name = forms.CharField()

class user_searchForm(forms.Form):
    name = forms.CharField()

class GenreForm(forms.Form):
    GENRES = [
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('action', 'Action'),
        ('horror', 'Horror'),
    ]
    genre = forms.ChoiceField(choices=GENRES)