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
        # Get all houses with member counts
        houses = House.objects.all().order_by('name')
        for house in houses:
            house.member_count = Character.objects.filter(house=house).count()
        context['houses'] = houses
        return context