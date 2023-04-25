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
    