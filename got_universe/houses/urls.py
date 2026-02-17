from django.urls import path
from . import views

urlpatterns = [
    path('ranking/', views.house_ranking, name='house_ranking'),
    path('', views.house_list, name='house_list'),
    path('<int:id>/', views.house_detail, name='house_detail'),
    path('network/', views.house_network, name='house_network'),

]

