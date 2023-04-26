from django.urls import path
from . import views

urlpatterns = [
    path('',views.start,name = 'boot'),
    path('sign_up/', views.sign_up, name='register'),
    path('search_anime/', views.search_anime, name='searchanime'),
    path('search_manga/', views.search_manga, name='searchmanga'),
    path('search_novel/', views.search_novel, name='searchnovel'),
    path('login/', views.login, name='login'),
    path('homepage/<str:username>/', views.homepage, name='home'),
    path('myprofile/<str:username>/', views.profile, name = 'myprofile'),
    path('friends/<str:username>/', views.friends, name = 'friends'),
    path('mylist/<str:username>/', views.mylist, name = 'mylist'),
    path('mylist_s/<str:username>/', views.mylist_s, name = 'mylist_s'),
    path('search_anime/<int:id>/',views.anime_profile,name = 'animeprofile'),
    path('userpage/<str:username>/<str:username2>/', views.userpage, name = 'userprofile'),
    path('inbox/<str:username>',views.inbox,name = 'inbox'),
    path('recommended/<str:username>/',views.recommend, name='recommended')
]
