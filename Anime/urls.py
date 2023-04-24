from django.urls import path
from . import views

urlpatterns = [
    path('search_anime/', views.search_anime, name='search'),
]
