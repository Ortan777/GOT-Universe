from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db import models
from django.db.models import Q
from .models import Character, House


# Helper function for house colors
def get_house_color(house_name):
    """Get color for a house"""
    colors = {
        'Targaryen': '#4A0404',
        'Stark': '#2C3E50',
        'Lannister': '#C5A028',
        'Baratheon': '#8B0000',
        'Greyjoy': '#2F4F4F',
        'Tyrell': '#228B22',
        'Martell': '#FF6B35',
        'Tully': '#1E4D6E',
        'Arryn': '#87CEEB',
        'Bolton': '#8B0000',
        'Frey': '#6B4F3C',
        'Mormont': '#2F4F4F',
        'Velaryon': '#1E4D6E',
        'Hightower': '#8B4513',
        'Dayne': '#4A4A4A',
        'Tarly': '#006400',
        'Clegane': '#4A4A4A',
    }
    return colors.get(house_name, '#4A4A4A')

class CharacterListView(ListView):
    model = Character
    template_name = 'characters/list.html'
    context_object_name = 'characters'
    paginate_by = 24
    
    def get_queryset(self):
        queryset = Character.objects.all().order_by('name')
        
        # Filter by house
        house_id = self.request.GET.get('house')
        if house_id:
            queryset = queryset.filter(house_id=house_id)
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(also_known_as__icontains=search_query) |
                Q(titles__icontains=search_query) |
                Q(culture__icontains=search_query) |
                Q(dragon__icontains=search_query) |
                Q(house__name__icontains=search_query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get ONLY houses that have at least one character
        houses_with_members = []
        all_houses = House.objects.all().order_by('name')
        
        for house in all_houses:
            member_count = Character.objects.filter(house=house).count()
            if member_count > 0:
                house.member_count = member_count
                houses_with_members.append(house)
        
        context['houses'] = houses_with_members
        context['title'] = 'Characters of Westeros'
        context['total_characters'] = Character.objects.count()
        context['total_houses_with_members'] = len(houses_with_members)
        context['total_houses'] = House.objects.count()
        
        # Pass search query back to template
        context['search_query'] = self.request.GET.get('search', '')
        
        # Add house colors to each character
        for character in context['characters']:
            if character.house:
                character.house_color = get_house_color(character.house.name)
            else:
                character.house_color = '#4A4A4A'
        
        return context

class CharacterDetailView(DetailView):
    """Show individual character details"""
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
        
        # Get children
        context['children'] = Character.objects.filter(
            models.Q(father=character) | models.Q(mother=character)
        )
        
        # Get siblings
        siblings = Character.objects.none()
        if character.father:
            siblings = siblings | Character.objects.filter(father=character.father).exclude(id=character.id)
        if character.mother:
            siblings = siblings | Character.objects.filter(mother=character.mother).exclude(id=character.id)
        context['siblings'] = siblings.distinct()
        
        # Add house color
        if character.house:
            context['house_color'] = get_house_color(character.house.name)
        
        return context

class HouseListView(ListView):
    """List all houses"""
    model = House
    template_name = 'houses/list.html'
    context_object_name = 'houses'
    
    def get_queryset(self):
        # Only show houses with members
        houses = House.objects.all().order_by('name')
        for house in houses:
            house.member_count = Character.objects.filter(house=house).count()
        return [h for h in houses if h.member_count > 0]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Great Houses of Westeros'
        return context

class HouseDetailView(DetailView):
    """Show individual house details"""
    model = House
    template_name = 'houses/detail.html'
    context_object_name = 'house'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = self.get_object()
        context['members'] = Character.objects.filter(house=house)
        context['house_color'] = get_house_color(house.name)
        return context