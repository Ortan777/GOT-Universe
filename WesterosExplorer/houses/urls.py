from django.urls import path
from . import views

urlpatterns = [
    path('', views.HouseListView.as_view(), name='house_list'),
]