from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up, name='register'),
    path('search_anime/', views.search_anime, name='search'),
    path('login/', views.login, name='log in'),
    path('homepage/<str:username>/', views.homepage, name='home')
]