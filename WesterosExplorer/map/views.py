# In map/views.py
from django.views.generic import TemplateView, DetailView
from .models import Location

class MapView(TemplateView):
    template_name = 'map/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Map of Westeros & Essos'
        context['locations'] = Location.objects.all()
        return context

class LocationDetailView(DetailView):
    model = Location
    template_name = 'map/location_detail.html'
    context_object_name = 'location'