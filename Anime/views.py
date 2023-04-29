from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.db import connection
from .forms import *
from datetime import date

# Create your views here.


def search_anime(request, username):   
    with connection.cursor() as cursor:
        cursor.execute("WITH temp AS (SELECT id,eng_title,japanese_title,episodes,CAST(EXTRACT(YEAR FROM aired_from) AS INTEGER) As year_from,COUNT(*) AS num_watched FROM Completed,Anime WHERE Anime.id = Completed.animeid AND Anime.source = %s GROUP BY id,eng_title,japanese_title,episodes,year_from), temp2 AS(SELECT id,eng_title,japanese_title,episodes,year_from,num_watched,rank() over(partition by year_from ORDER BY num_watched DESC) AS row_num FROM temp ) SELECT id,eng_title,japanese_title,episodes,year_from FROM temp2 WHERE row_num = 1 ORDER BY year_from DESC;", ['Original'])
        yearly_list = cursor.fetchall()
        cursor.execute("WITH temp AS(SELECT animeid,COUNT(*) as num_users FROM Favourites WHERE Source = %s GROUP BY animeid ORDER BY num_users DESC LIMIT 10) SELECT  ID,eng_title,japanese_title,episodes,anime.score FROM temp,anime WHERE animeid = id;", ['Original'])
        mostfav_list = cursor.fetchall()   
    if request.method == 'POST':   
        val = request.POST.get('type')  
        if (val=='1'):
            genre_form = GenreForm(request.POST)
            if genre_form.is_valid():
                genre = genre_form.cleaned_data['genre']
                form = SearchForm()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime WHERE %s = ANY(genres) AND source = %s ORDER BY score DESC LIMIT 10;",[genre,'Original'])
                    top_list = cursor.fetchall()
        else:
            form = SearchForm(request.POST)
            if form.is_valid():
                anime_title = form.cleaned_data['anime_title']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE (eng_title ILIKE %s OR japanese_title ILIKE %s) AND source = %s;", ['%{}%'.format(anime_title),'%{}%'.format(anime_title), 'Original'])
                    anime_list = cursor.fetchall()
            return render(request, 'anime_results.html', {'anime_list': anime_list, 'username': username})
    else:
        form = SearchForm()
        genre_form = GenreForm()   
        with connection.cursor() as cursor:
            cursor.execute("SELECT  Anime.ID,eng_title,japanese_title,episodes,score FROM Anime  WHERE source = %s ORDER BY score DESC LIMIT 10;",['Original'])
            top_list = cursor.fetchall()      
    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list' : top_list, 'genre_form': genre_form, 'username': username })


def search_manga(request, username):       
    with connection.cursor() as cursor:
        cursor.execute("WITH temp AS (SELECT id,eng_title,japanese_title,episodes,CAST(EXTRACT(YEAR FROM aired_from) AS INTEGER) As year_from,COUNT(*) AS num_watched FROM Completed,Anime WHERE Anime.id = Completed.animeid AND Anime.source = %s GROUP BY id,eng_title,japanese_title,episodes,year_from), temp2 AS(SELECT id,eng_title,japanese_title,episodes,year_from,num_watched,rank() over(partition by year_from ORDER BY num_watched DESC) AS row_num FROM temp ) SELECT id,eng_title,japanese_title,episodes,year_from FROM temp2 WHERE row_num = 1 ORDER BY year_from DESC;", ['Manga'])
        yearly_list = cursor.fetchall()
        cursor.execute("WITH temp AS(SELECT animeid,COUNT(*) as num_users FROM Favourites WHERE Source = %s GROUP BY animeid ORDER BY num_users DESC LIMIT 10) SELECT  ID,eng_title,japanese_title,episodes,anime.score FROM temp,anime WHERE animeid = id;", ['Manga'])
        mostfav_list = cursor.fetchall()        
    if request.method == 'POST':   
        val = request.POST.get('type')   
        genre_form = GenreForm(request.POST)
        form = SearchForm(request.POST)
        if (val == '1'):
            genre_form = GenreForm(request.POST)
            if genre_form.is_valid():
                genre = genre_form.cleaned_data['genre']
                form = SearchForm()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime WHERE %s = ANY(genres) AND source = %s ORDER BY score DESC LIMIT 10;",[genre,'Manga'])
                    top_list = cursor.fetchall()           
        else:
            form = SearchForm(request.POST)
            if form.is_valid():
                anime_title = form.cleaned_data['anime_title']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE (eng_title ILIKE %s OR japanese_title ILIKE %s) AND source = %s;", ['%{}%'.format(anime_title),'%{}%'.format(anime_title), 'Manga'])
                    print("manga")
                    anime_list = cursor.fetchall()
                return render(request, 'anime_results.html', {'anime_list': anime_list, 'username': username})
    else:
        form = SearchForm()
        genre_form = GenreForm()
        with connection.cursor() as cursor:
            cursor.execute("SELECT Anime.ID,eng_title,japanese_title,episodes,score FROM Anime  WHERE source = %s ORDER BY score DESC LIMIT 10;",['Manga'])
            top_list = cursor.fetchall()

    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list' : top_list, 'genre_form': genre_form, 'username': username })

def search_novel(request, username):   
    with connection.cursor() as cursor:
        cursor.execute("WITH temp AS (SELECT id,eng_title,japanese_title,episodes,CAST(EXTRACT(YEAR FROM aired_from) AS INTEGER) As year_from,COUNT(*) AS num_watched FROM Completed,Anime WHERE Anime.id = Completed.animeid AND Anime.source ILIKE %s GROUP BY id,eng_title,japanese_title,episodes,year_from), temp2 AS(SELECT id,eng_title,japanese_title,episodes,year_from,num_watched,rank() over(partition by year_from ORDER BY num_watched DESC) AS row_num FROM temp ) SELECT id,eng_title,japanese_title,episodes,year_from FROM temp2 WHERE row_num = 1 ORDER BY year_from DESC;", ['%{}%'.format('novel')])
        yearly_list = cursor.fetchall()
        cursor.execute("WITH temp AS(SELECT animeid,COUNT(*) as num_users FROM Favourites WHERE Source ILIKE %s GROUP BY animeid ORDER BY num_users DESC LIMIT 10) SELECT ID,eng_title,japanese_title,episodes,anime.score FROM temp,anime WHERE animeid = id;", ['%{}%'.format('novel')])
        mostfav_list = cursor.fetchall()        
    if request.method == 'POST':   
        val = request.POST.get('type')   
        if (val == '1'):
            genre_form = GenreForm(request.POST)
            if genre_form.is_valid():
                genre = genre_form.cleaned_data['genre']
                form = SearchForm()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime WHERE %s = ANY(genres) AND source ILIKE %s ORDER BY score DESC LIMIT 10;",[genre, '%{}%'.format('novel')])
                    top_list = cursor.fetchall()              
        else:       
            form = SearchForm(request.POST)
            if form.is_valid():
                anime_title = form.cleaned_data['anime_title']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id,eng_title,japanese_title,episodes,aired_from,aired_to FROM Anime WHERE (eng_title ILIKE %s OR japanese_title ILIKE %s) AND source ILIKE %s;", ['%{}%'.format(anime_title),'%{}%'.format(anime_title), '%{}%'.format('novel')])
                    anime_list = cursor.fetchall()
                return render(request, 'anime_results.html', {'anime_list': anime_list, 'username': username})
    else:
        form = SearchForm()
        genre_form = GenreForm()
        with connection.cursor() as cursor:
            cursor.execute("SELECT  Anime.ID,eng_title,japanese_title,episodes,score FROM Anime  WHERE source ILIKE %s ORDER BY score DESC LIMIT 10;",['%{}%'.format('novel')])
            top_list = cursor.fetchall()
    # Render the search template with the search form
    return render(request, 'anime_search.html', {'form': form, 'yearly_list': yearly_list, 'mostfav_list': mostfav_list, 'top_list' : top_list, 'genre_form': genre_form, 'username': username })

def sign_up(request):
    confirm_flag = False
    name_flag = False
    flag = True
    if request.method == 'POST':
        form = Sign_upForm(request.POST)
        if form.is_valid():
            I1 = form.cleaned_data['Name']
            I6 = form.cleaned_data['Password']
            I7 = form.cleaned_data['Confirm_password']
            I2 = form.cleaned_data['Gender']
            I3 = form.cleaned_data['Birthdate']
            I4 = form.cleaned_data['Location']
            I5 = date.today()
            with connection.cursor() as cursor:
                cursor.execute("Select name from Users where name = %s",[I1])
                if(len(cursor.fetchall())):
                    form = Sign_upForm()
                    name_flag = True
                    flag = False
                    return render(request, 'signup.html', {'form': form, 'flag': flag, 'name_flag': name_flag, 'confirm_flag': confirm_flag})   
            if(I6 != I7):
                form = Sign_upForm() 
                confirm_flag = True 
                flag = False
                return render(request, 'signup.html', {'form': form, 'flag': flag, 'name_flag': name_flag, 'confirm_flag': confirm_flag})                      
            with connection.cursor() as cursor:
                cursor.execute("Insert Into Users(name, gender, birthdate, location, joindate, inbox, password) values(%s, %s, %s, %s, %s, '{}', %s);", [I1, I2, I3, I4, I5, I6])
                cursor.execute("INSERT INTO Stats(name,num_completed,episodes_watched,num_watching,num_planning) values(%s,0,0,0,0);",[I1])
            # Render the results template with the list of anime
            return redirect('/login/')
    else:
        form = Sign_upForm()    
    # Render the search template with the search form
    return render(request, 'signup.html', {'form': form, 'flag': flag, 'name_flag': name_flag, 'confirm_flag': confirm_flag})


def login(request):
    user_flag = False
    passcode_flag = False
    flag = True
    if request.method == 'POST':
        form = log_inForm(request.POST)
        if form.is_valid():
            I1 = form.cleaned_data['Username']
            I2 = form.cleaned_data['Password']
            with connection.cursor() as cursor:
                cursor.execute("Select name, password from Users where name = %s",[I1])
                up_list = cursor.fetchall()
                if(len(up_list)==0):
                    form = log_inForm()
                    user_flag = True
                    flag = False
                    return render(request, 'login.html', {'form': form, 'flag': flag, 'user_flag': user_flag, 'passcode_flag': passcode_flag})
                else:
                    if(up_list[0][1] != I2):
                        form = log_inForm()
                        passcode_flag = True
                        flag = False
                        return render(request, 'login.html', {'form': form, 'flag': flag, 'user_flag': user_flag, 'passcode_flag': passcode_flag})
                
            return redirect('/homepage/{}/'.format(I1))
    else:
        form = log_inForm()    
    # Render the search template with the search form
    return render(request, 'login.html', {'form': form, 'flag': flag, 'user_flag': user_flag, 'passcode_flag': passcode_flag})


def homepage(request, username):
    if request.method == 'POST':
        form = user_searchForm(request.POST)
        if form.is_valid():
            # Get the Japanese title from the form
            user_name = form.cleaned_data['name']
            # Query the database for anime with the given Japanese title
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM users WHERE name = %s AND name != %s;", [user_name,username])
                user = cursor.fetchall()
            # Render the results template with the list of anime
                if(len(user) == 0):
                    return render(request,"second.html")
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
            cursor.execute("SELECT inbox FROM users WHERE name = ''")
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
    return render(request,'friends.html',{'friends':friends,'username':username})

def mylist(request,username):
    flag = False
    return render(request,'mylist.html', {'username' :username, 'flag' :flag})

def mylist_s(request, username):
    query = request.GET.get('status', '')
    flag = True
    if request.method == 'POST':
        id = int(request.POST.get('type'))
        score = int(request.POST['score'])
        with connection.cursor() as cursor:
            if(score == 0):
                cursor.execute("DELETE FROM Completed WHERE name= %s AND animeid = %s;",[username, id])    
            else:
                cursor.execute("UPDATE Completed SET score = %s WHERE animeid = %s AND name = %s;", [score, id, username])
                cursor.execute("UPDATE Anime SET num_scored_by =num_scored_by +1,score = ((SELECT score FROM Anime WHERE id = %s)*(num_scored_by-1)*(1.0) + %s *(1.0))/(num_scored_by) WHERE ID = %s;",[id,score,id])

    with connection.cursor() as cursor:
        if(query == '1'):
            cursor.execute("WITH temp AS (SELECT animeid,score FROM completed WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,temp.score FROM anime, temp WHERE animeid=ID;", [username])
        elif(query == '2'):
            cursor.execute("WITH temp AS (SELECT animeid FROM planning WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,score FROM anime, temp WHERE animeid=ID;", [username])
        elif(query == '4'):
            cursor.execute("WITH temp AS (SELECT animeid FROM watching WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,score FROM anime, temp WHERE animeid=ID;", [username])
        elif(query == '3'):
            cursor.execute("WITH temp AS (SELECT animeid FROM Favourites WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,score FROM anime, temp WHERE animeid=ID;", [username])
        else:
            flag = False
        anime_list = []
        for row in cursor.fetchall():
            anime_list.append({
                "id": row[0],
                "eng": row[1],
                "jap": row[2],
                "epi": row[3],
                "from": row[4],
                "to": row[5],
                "score": row[6]
            })
    return render(request, 'mylist.html', {'username' :username, 'flag' :flag, 'anime_list' :anime_list, 'query' : query})
    
def start(request):
    return render(request,'start.html')

def anime_profile(request,username,id):
    if request.method == 'POST':
        val_h = request.POST.get('type') 
        if(val_h == '1'):
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO favourites(name, animeid) VALUES (%s, %s);",(username,id))
            return redirect('/homepage/{}/'.format(username))
        else:
            status = request.POST['status']
            if status == 'watching':
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM watching WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM completed WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM planning WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("INSERT INTO watching(name, animeid) VALUES (%s, %s);",(username,id))
                return redirect('/homepage/{}/'.format(username))
            elif status == 'completed':
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM watching WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM completed WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM planning WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("INSERT INTO completed(name, animeid) VALUES (%s, %s);",(username,id))
                return redirect('/homepage/{}/'.format(username))
            elif status == 'planning':
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM watching WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM completed WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM planning WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("INSERT INTO planning(name, animeid) VALUES (%s, %s);",(username,id))
                return redirect('/homepage/{}/'.format(username))
            else:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM watching WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM completed WHERE name= %s AND animeid = %s;",(username,id))
                    cursor.execute("DELETE FROM planning WHERE name= %s AND animeid = %s;",(username,id)) 
                return redirect('/homepage/{}/'.format(username))

    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Anime WHERE id = %s;", [id])
            anime = cursor.fetchall()[0]
        val = 0
        val_f = False
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM watching where name = %s AND animeid = %s",(username,id))
            l = cursor.fetchall()
            if(len(l) != 0):
                val = 1
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM completed where name = %s AND animeid = %s",(username,id))
            l = cursor.fetchall()
            if(len(l) != 0):
                val = 2
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM planning where name = %s AND animeid = %s",(username,id))
            l = cursor.fetchall()
            if(len(l) != 0):
                val = 3
                
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM favourites where name = %s AND animeid = %s",(username,id))
            l = cursor.fetchall()
            if(len(l) != 0):
                val_f = True
        return render(request,'anime_profile.html',{'anime':anime,'val':val, 'val_f': val_f, 'username': username})

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
        cursor.execute("WITH temp AS(SELECT genre FROM Genre_count WHERE name = %s ORDER BY count DESC LIMIT 2), temp2 as (SELECT DISTINCT ID,eng_title,japanese_title,episodes,aired_from,aired_to,source,score,genres FROM temp,anime WHERE genre = ANY(genres) AND ID NOT IN (SELECT animeid FROM Completed WHERE name = %s)  ORDER BY score DESC LIMIT 50) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,source,genres FROM temp2;",[username,username])
        anime_list = cursor.fetchall()
    return render(request,'recommended.html',{'username':username,'anime_list': anime_list})

def friendprofile(request,username,username1):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Stats WHERE name = %s;", [username1])
        stats = cursor.fetchall()
    flag = False
    return render(request,'friendprofile.html', {'username' :username, 'flag' :flag ,'stats':stats , 'username1':username1})

def friendprofile_s(request,username,username1):
    query = request.GET.get('status', '')
    flag = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Stats WHERE name = %s;", [username1])
        stats = cursor.fetchall()
    with connection.cursor() as cursor:
        if(query == '1'):
            cursor.execute("WITH temp AS (SELECT animeid,score FROM completed WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to,temp.score FROM anime, temp WHERE animeid=ID;", [username1])
        elif(query == '2'):
            cursor.execute("WITH temp AS (SELECT animeid FROM planning WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;", [username1])
        elif(query == '4'):
            cursor.execute("WITH temp AS (SELECT animeid FROM watching WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;", [username1])
        elif(query == '3'):
            cursor.execute("WITH temp AS (SELECT animeid FROM Favourites WHERE name =%s ) SELECT ID,eng_title,japanese_title,episodes,aired_from,aired_to FROM anime, temp WHERE animeid=ID;", [username1])
        else:
            flag = False
        anime_list = cursor.fetchall()
    return render(request, 'friendprofile.html', {'username' :username, 'flag' :flag, 'anime_list' :anime_list, 'query' : query , 'username1':username1 , 'stats' : stats})



def my_view(request):
    username1 = 'example_user'
    # other code here to get stats and anime_list
    context = {'stats': stats, 'anime_list': anime_list, 'username1': username1}
    return render(request, 'my_template.html', context)





    