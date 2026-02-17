from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.map_view, name='map_view'),
    path('', views.location_list, name='location_list'),
    path('<int:id>/', views.location_detail, name='location_detail'),
]

