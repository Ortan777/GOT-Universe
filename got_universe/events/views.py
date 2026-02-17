from django.shortcuts import render
from .models import Event


def event_list(request):
    season = request.GET.get('season')

    events = Event.objects.all().order_by('season', 'episode')

    if season:
        events = events.filter(season=season)

    context = {
        'events': events,
        'selected_season': season,
        'seasons': Event.objects.values_list('season', flat=True).distinct().order_by('season')
    }

    return render(request, 'events/event_list.html', context)
