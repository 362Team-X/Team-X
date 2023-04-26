from django import forms

class SearchForm(forms.Form):
    anime_title = forms.CharField()
    
class Sign_upForm(forms.Form):
    name = forms.CharField()
    passcode = forms.CharField()
    confirm_passcode = forms.CharField()
    gender = forms.CharField()
    birthdate = forms.DateField()
    location = forms.CharField()
    
class log_inForm(forms.Form):
    name = forms.CharField()
    passcode = forms.CharField()    

class user_searchForm(forms.Form):
    name = forms.CharField()

class GenreForm(forms.Form):
    GENRES = [        
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Cars', 'Cars'),
        ('Comedy', 'Comedy'),
        ('Demons', 'Demons'),
        ('Drama', 'Drama'),
        ('Game', 'Game'),
        ('Harem', 'Harem'),
        ('Hentai', 'Hentai'),
        ('Vampire', 'Vampire'),
    ]
    genre = forms.ChoiceField(choices=GENRES)