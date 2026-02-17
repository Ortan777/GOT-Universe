from django.shortcuts import render
from django.views.generic import TemplateView

class TimelineView(TemplateView):
    template_name = 'timeline/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Timeline of Events'
        return context