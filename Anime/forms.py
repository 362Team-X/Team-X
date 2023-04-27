from django import forms

class SearchForm(forms.Form):
    anime_title = forms.CharField()
    
class Sign_upForm(forms.Form):
    Name = forms.CharField()
    Password = forms.CharField(widget=forms.PasswordInput)
    Confirm_password = forms.CharField(widget=forms.PasswordInput)
    Gender = forms.CharField()
    Birthdate = forms.DateField()
    Location = forms.CharField()
    
class log_inForm(forms.Form):
    Username = forms.CharField()
    Password = forms.CharField(widget=forms.PasswordInput)    

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
    