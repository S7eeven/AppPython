from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_pokemon/', views.search_pokemon, name='search_pokemon'),
    path('pokemon/<str:pokemon_name>/', views.pokemon_detail, name='pokemon_detail'),
]