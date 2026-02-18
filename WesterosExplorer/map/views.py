from django.shortcuts import render
from django.views.generic import TemplateView

class MapView(TemplateView):
    template_name = 'map/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Map of Westeros & Essos'
        return context