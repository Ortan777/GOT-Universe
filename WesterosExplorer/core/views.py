from django.shortcuts import render
from django.views.generic import TemplateView
from characters.models import House, Character

class HomeView(TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_characters'] = [
            {
                'name': 'Daenerys Targaryen',
                'quote': 'Fire cannot kill a dragon.',
                'image': 'dany.jpg',
                'house': 'Targaryen'
            },
            {
                'name': 'Jon Snow',
                'quote': 'I am the watcher on the walls.',
                'image': 'jon.jpg',
                'house': 'Stark'
            },
            {
                'name': 'Tyrion Lannister',
                'quote': 'I drink and I know things.',
                'image': 'tyrion.jpg',
                'house': 'Lannister'
            },
        ]
        return context

class FamilyTreeView(TemplateView):
    template_name = 'pages/family_tree.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get ONLY houses that have at least one character
        houses = []
        all_houses = House.objects.all().order_by('name')
        
        for house in all_houses:
            member_count = Character.objects.filter(house=house).count()
            if member_count > 0:
                house.member_count = member_count
                houses.append(house)
        
        context['houses'] = houses
        context['total_houses_with_members'] = len(houses)
        context['total_houses'] = House.objects.count()
        
        return context

class TestCardsView(TemplateView):
    template_name = 'pages/test_cards.html'