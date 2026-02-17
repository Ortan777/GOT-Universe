from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db import models  # Add this
from characters.models import House, Character

class HouseListView(ListView):
    model = House
    template_name = 'houses/list.html'
    context_object_name = 'houses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Great Houses of Westeros'
        return context

class HouseDetailView(DetailView):
    model = House
    template_name = 'houses/detail.html'
    context_object_name = 'house'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = self.get_object()
        context['members'] = Character.objects.filter(house=house)
        return context