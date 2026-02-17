from django.urls import path
from . import views

urlpatterns = [
    path('', views.CharacterListView.as_view(), name='character_list'),
    path('<int:pk>/', views.CharacterDetailView.as_view(), name='character_detail'),
]