from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.db import connection
from .forms import *
from datetime import date

# Create your views here.
def home(request):
    return HttpResponse("Welcome to anime recommender")

def search_anime(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Get the Japanese title from the form
            anime_title = form.cleaned_data['anime_title']
            source = form.cleaned_data['source']
            
            # Query the database for anime with the given Japanese title
            with connection.cursor() as cursor:
                cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE (eng_title ILIKE %s OR japanese_title ILIKE %s) AND source = %s;", ['%{}%'.format(anime_title),'%{}%'.format(anime_title),source])
                anime_list = cursor.fetchall()
            # Render the results template with the list of anime
            return render(request, 'anime_results.html', {'anime_list': anime_list})
    else:
        form = SearchForm()
        
    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = Sign_upForm(request.POST)
        if form.is_valid():
            I1 = form.cleaned_data['name']
            I2 = form.cleaned_data['gender']
            I3 = form.cleaned_data['birthdate']
            I4 = form.cleaned_data['location']
            I5 = date.today()
            with connection.cursor() as cursor:
                cursor.execute("Insert Into Users(name, gender, birthdate, location, joindate, inbox) values(%s, %s, %s, %s, %s, '{}')", [I1, I2, I3, I4, I5])
            # Render the results template with the list of anime
            return redirect('/login/')
    else:
        form = Sign_upForm()    
    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = log_inForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            return redirect('/homepage/{}/'.format(username))
    else:
        form = log_inForm()    
    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form})

def homepage(request, username):
    return render(request, 'first.html')


    