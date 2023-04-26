from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.db import connection
from .forms import *
from datetime import date

# Create your views here.
def home(request):
    return HttpResponse("Welcome to anime recommender")

def search_anime(request):
    
    with connection.cursor() as cursor:
        cursor.execute("WITH temp AS (SELECT id,eng_title,japanese_title,episodes,EXTRACT(YEAR FROM aired_from) As year_from,COUNT(*) AS num_watched FROM Completed,Anime WHERE Anime.id = Completed.animeid AND Anime.source = %s GROUP BY id,eng_title,japanese_title,episodes,year_from), temp2 AS(SELECT id,eng_title,japanese_title,episodes,year_from,num_watched,rank() over(partition by year_from ORDER BY num_watched DESC) AS row_num FROM temp ) SELECT id,eng_title,japanese_title,episodes,year_from FROM temp2 WHERE row_num = 1 ORDER BY year_from DESC;", ['Original'])
        yearly_list = cursor.fetchall()
        cursor.execute("WITH temp AS(SELECT animeid,COUNT(*) as num_users FROM Favourites WHERE Source = %s GROUP BY animeid ORDER BY num_users DESC LIMIT 10) SELECT  ID,eng_title,japanese_title,episodes,anime.score FROM temp,anime WHERE animeid = id;", ['Original'])
        mostfav_list = cursor.fetchall()   
    form = SearchForm()
    genre_form = GenreForm()
    if request.method == 'POST':   
        val = request.POST.get('type')   
        if val:
            genre_form = GenreForm(request.POST)
            if form.is_valid():
                genre = form.cleaned_data['genre']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime WHERE %s = ANY(genres) AND source = %s LIMIT 20;",[genre,'Original'])
                    top_list = cursor.fetchall()
                    return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list' : top_list, 'genre_form': genre_form })
        else:
            form = SearchForm(request.POST)
            if form.is_valid():
                anime_title = form.cleaned_data['anime_title']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE (eng_title ILIKE %s OR japanese_title ILIKE %s) AND source = %s;", ['%{}%'.format(anime_title),'%{}%'.format(anime_title), 'Original'])
                    anime_list = cursor.fetchall()
            return render(request, 'anime_results.html', {'anime_list': anime_list})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT  Anime.ID,eng_title,japanese_title,episodes,score FROM Anime  WHERE source = %s ORDER BY score DESC LIMIT 10;",['Original'])
            top_list = cursor.fetchall()
            return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list' : top_list, 'genre_form': genre_form })
        

    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list' : top_list, 'genre_form': genre_form })


def search_manga(request):   
    
    with connection.cursor() as cursor:
        cursor.execute("WITH temp AS (SELECT id,eng_title,japanese_title,episodes,EXTRACT(YEAR FROM aired_from) As year_from,COUNT(*) AS num_watched FROM Completed,Anime WHERE Anime.id = Completed.animeid AND Anime.source = %s GROUP BY id,eng_title,japanese_title,episodes,year_from), temp2 AS(SELECT id,eng_title,japanese_title,episodes,year_from,num_watched,rank() over(partition by year_from ORDER BY num_watched DESC) AS row_num FROM temp ) SELECT id,eng_title,japanese_title,episodes,year_from FROM temp2 WHERE row_num = 1 ORDER BY year_from DESC;", ['Manga'])
        yearly_list = cursor.fetchall()
        cursor.execute("WITH temp AS(SELECT animeid,COUNT(*) as num_users FROM Favourites WHERE Source = %s GROUP BY animeid ORDER BY num_users DESC LIMIT 10) SELECT  ID,eng_title,japanese_title,episodes,anime.score FROM temp,anime WHERE animeid = id;", ['Manga'])
        mostfav_list = cursor.fetchall()
        
    if request.method == 'POST':   
        val = request.POST.get('type')   
        if val:
            form = GenreForm(request.POST)
            if form.is_valid():
                genre = form.cleaned_data['genre']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime WHERE %s = ANY(genres) AND source = %s LIMIT 20;",[genre,'Manga'])
                    top_list = cursor.fetchall()           
        else:
            form = SearchForm(request.POST)
            if form.is_valid():
                anime_title = form.cleaned_data['anime_title']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE (eng_title ILIKE %s OR japanese_title ILIKE %s) AND source = %s;", ['%{}%'.format(anime_title),'%{}%'.format(anime_title), 'Manga'])
                    print("manga")
                    anime_list = cursor.fetchall()
                return render(request, 'anime_results.html', {'anime_list': anime_list})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Anime.ID,eng_title,japanese_title,episodes,score FROM Anime  WHERE source = %s ORDER BY score DESC LIMIT 10;",['Manga'])
            top_list = cursor.fetchall()
        form = SearchForm()
        genre_form = GenreForm()

    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list': top_list})

def search_novel(request):
    
    with connection.cursor() as cursor:
        cursor.execute("WITH temp AS (SELECT id,eng_title,japanese_title,episodes,EXTRACT(YEAR FROM aired_from) As year_from,COUNT(*) AS num_watched FROM Completed,Anime WHERE Anime.id = Completed.animeid AND Anime.source ILIKE %s GROUP BY id,eng_title,japanese_title,episodes,year_from), temp2 AS(SELECT id,eng_title,japanese_title,episodes,year_from,num_watched,rank() over(partition by year_from ORDER BY num_watched DESC) AS row_num FROM temp ) SELECT id,eng_title,japanese_title,episodes,year_from FROM temp2 WHERE row_num = 1 ORDER BY year_from DESC;", ['%{}%'.format('novel')])
        yearly_list = cursor.fetchall()
        cursor.execute("WITH temp AS(SELECT animeid,COUNT(*) as num_users FROM Favourites WHERE Source ILIKE %s GROUP BY animeid ORDER BY num_users DESC LIMIT 10) SELECT ID,eng_title,japanese_title,episodes,anime.score FROM temp,anime WHERE animeid = id;", ['%{}%'.format('novel')])
        mostfav_list = cursor.fetchall()
        
    if request.method == 'POST':   
        val = request.POST.get('type')   
        if val:
            form = GenreForm(request.POST)
            if form.is_valid():
                genre = form.cleaned_data['genre']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime WHERE %s = ANY(genres) AND source ILIKE %s LIMIT 20;",[genre, '%{}%'.format('novel')])
                    top_list = cursor.fetchall()              
        else:       
            form = SearchForm(request.POST)
            if form.is_valid():
                anime_title = form.cleaned_data['anime_title']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE (eng_title ILIKE %s OR japanese_title ILIKE %s) AND source ILIKE %s;", ['%{}%'.format(anime_title),'%{}%'.format(anime_title), '%{}%'.format('novel')])
                    anime_list = cursor.fetchall()
                return render(request, 'anime_results.html', {'anime_list': anime_list})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT  Anime.ID,eng_title,japanese_title,episodes,score FROM Anime  WHERE source ILIKE %s ORDER BY score DESC LIMIT 10;",['%{}%'.format('novel')])
            top_list = cursor.fetchall()
        form = SearchForm()

    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list': top_list})

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
                cursor.execute("Insert Into Users(name, gender, birthdate, location, joindate, inbox) values(%s, %s, %s, %s, %s, '{}');", [I1, I2, I3, I4, I5])
                cursor.execute("INSERT INTO Stats(name,num_completed,episodes_watched,num_watching,num_planning) values(%s,0,0,0,0);",[I1])
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
    return render(request, 'login.html', {'form': form})


def homepage(request, username):
    if request.method == 'POST':
        form = user_searchForm(request.POST)
        if form.is_valid():
            # Get the Japanese title from the form
            user_name = form.cleaned_data['name']
            # Query the database for anime with the given Japanese title
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM users WHERE name = %s;", [user_name])
                user = cursor.fetchall()
            # Render the results template with the list of anime
                return redirect('/userpage/{}/{}/'.format(username, user[0][0]))
    else:
        form = user_searchForm()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to,source FROM Anime ORDER BY score DESC LIMIT 50;") 
            anime_list = cursor.fetchall() 
    return render(request,'homepage.html', {'username' :username,'form' : form,'anime_list': anime_list})


def userpage(request, username, username2):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Users SET inbox = array_append(inbox,%s) WHERE name = %s;",[username,username2])
        return render(request,'first.html')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Stats WHERE name = %s;", [username2])
            stats = cursor.fetchall()
        return render(request,'userprofile.html',{'stats':stats, 'username' : username})

def profile(request,username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Stats WHERE name = %s;", [username])
        stats = cursor.fetchall()
    return render(request,'myprofile.html',{'stats':stats})

def friends(request,username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name1 FROM friends WHERE name2 = %s UNION SELECT name2 FROM friends WHERE name1 = %s;", [username, username])
        friends = cursor.fetchall()
    return render(request,'friends.html',{'friends':friends})

def mylist(request,username):
    flag = False
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Stats WHERE name = %s;", [username])
        friends = cursor.fetchall()
    return render(request,'mylist.html', {'username' :username, 'flag' :flag})

def mylist_s(request, username):
    query = request.GET.get('status', '')
    flag = True
    with connection.cursor() as cursor:
        if(query == '1'):
            cursor.execute("WITH temp AS (SELECT animeid,score FROM completed WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,temp.score FROM anime, temp WHERE animeid=ID;", [username])
        elif(query == '2'):
            cursor.execute("WITH temp AS (SELECT animeid FROM planning WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;", [username])
        elif(query == '4'):
            cursor.execute("WITH temp AS (SELECT animeid FROM watching WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;", [username])
        elif(query == '3'):
            cursor.execute("WITH temp AS (SELECT animeid FROM Favourites WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;", [username])
        else:
            flag = False
        anime_list = cursor.fetchall()
    return render(request, 'mylist.html', {'username' :username, 'flag' :flag, 'anime_list' :anime_list, 'query' : query})
    
def start(request):
    return render(request,'start.html')

def anime_profile(request,id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Anime WHERE id = %s;", [id])
        anime = cursor.fetchall()[0]
    return render(request,'anime_profile.html',{'anime':anime})

def inbox(request,username):
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('user_name')
        if action == 'accept':
            with connection.cursor() as cursor:
                if(username < name):
                    cursor.execute("BEGIN TRANSACTION;INSERT INTO Friends(name1,name2)VALUES(%s,%s) ;UPDATE Users SET inbox = array_remove(inbox,%s) WHERE name = %s;END TRANSACTION;",[username,name,name,username])
                else:
                    cursor.execute("BEGIN TRANSACTION;INSERT INTO Friends(name1,name2)VALUES(%s,%s) ;UPDATE Users SET inbox = array_remove(inbox,%s) WHERE name = %s;END TRANSACTION;",[name,username,name,username])
        elif action == 'reject':
            with connection.cursor() as cursor:
                cursor.execute("UPDATE Users SET inbox = array_remove(inbox,%s) WHERE name = %s;",[name,username])
        return redirect('/homepage/{}/'.format(username))


    else:
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT inbox FROM users WHERE name = %s;", [username])
            users = cursor.fetchall()[0][0]
            print(users)

    return render(request,'inbox.html',{'users':users})

def recommend(request,username):
    with connection.cursor() as cursor:
        cursor.execute("WITH temp AS(SELECT genre FROM Genre_count WHERE name = '0' ORDER BY count DESC LIMIT 2), temp2 as (SELECT DISTINCT ID,eng_title,japanese_title,episodes,aired_from,aired_to,source,score,genres FROM temp,anime WHERE genre = ANY(genres)  ORDER BY score DESC LIMIT 50) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,source,genres FROM temp2;")
        anime_list = cursor.fetchall()
    return render(request,'recommended.html',{'username':username,'anime_list': anime_list})









    