# In map/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MapView.as_view(), name='map_view'),
    path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
]