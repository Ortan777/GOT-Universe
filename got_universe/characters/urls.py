from django.urls import path
from . import views

urlpatterns = [
    path('graph/', views.character_graph, name='character_graph'),
    path('ranking/', views.character_ranking, name='character_ranking'),
    path('compare/', views.compare_characters, name='compare_characters'),
    path('', views.character_list, name='character_list'),
    path('<int:id>/', views.character_detail, name='character_detail'),
]


