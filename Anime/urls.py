from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up, name='register'),
    path('search_anime/', views.search_anime, name='searchanime'),
    path('search_anime/', views.search_manga, name='searchmanga'),
    path('search_anime/', views.search_novel, name='searchnovel'),
    path('login/', views.login, name='log in'),
    path('homepage/<str:username>/', views.homepage, name='home'),
    path('myprofile/<str:username>/', views.profile, name = 'myprofile'),
    path('friends/<str:username>/', views.friends, name = 'friends'),
    path('mylist/<str:username>/', views.mylist, name = 'mylist'),
]