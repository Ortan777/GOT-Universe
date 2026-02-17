from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import models  # IMPORTANT: Add this import!
from .models import Character, House

class CharacterListView(ListView):
    model = Character
    template_name = 'characters/list.html'
    context_object_name = 'characters'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Character.objects.all().order_by('name')
        # Filter by house if specified
        house_id = self.request.GET.get('house')
        if house_id:
            queryset = queryset.filter(house_id=house_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['houses'] = House.objects.all()
        context['title'] = 'Characters of Westeros'
        context['total_characters'] = Character.objects.count()
        return context

class CharacterDetailView(DetailView):
    model = Character
    template_name = 'characters/detail.html'
    context_object_name = 'character'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = self.get_object()
        
        # Get family relations
        if character.father:
            context['father'] = character.father
        if character.mother:
            context['mother'] = character.mother
        
        # Get children - Fix the Q object usage
        context['children'] = Character.objects.filter(
            models.Q(father=character) | models.Q(mother=character)
        )
        
        # Get siblings (same father or mother)
        siblings = Character.objects.none()
        if character.father:
            siblings = siblings | Character.objects.filter(father=character.father).exclude(id=character.id)
        if character.mother:
            siblings = siblings | Character.objects.filter(mother=character.mother).exclude(id=character.id)
        context['siblings'] = siblings.distinct()
        
        return context

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