from django.shortcuts import render
from django.views.generic import ListView, DetailView  # Add this line!
from django.db import models
from characters.models import House, Character

class HouseListView(ListView):
    model = House
    template_name = 'houses/list.html'
    context_object_name = 'houses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Great Houses of Westeros'
        
        # Add member count
        for house in context['houses']:
            house.member_count = Character.objects.filter(house=house).count()
        
        return context

class HouseDetailView(DetailView):
    model = House
    template_name = 'houses/detail.html'
    context_object_name = 'house'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = self.get_object()
        context['members'] = Character.objects.filter(house=house).order_by('name')
        context['member_count'] = context['members'].count()
        return context