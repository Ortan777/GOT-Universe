from django.urls import path
from . import views_api

urlpatterns = [
    path('family-tree/', views_api.family_tree_data, name='api_family_tree'),
    path('houses/', views_api.house_list_api, name='api_houses'),
    path('character/<int:character_id>/', views_api.character_detail_api, name='api_character_detail'),
]