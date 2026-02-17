from django.urls import path
from . import views

urlpatterns = [
    path('family-tree/', views.FamilyTreeView.as_view(), name='family_tree'),
]