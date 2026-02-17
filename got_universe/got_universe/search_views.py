from django.shortcuts import render
from characters.models import Character
from houses.models import House
from events.models import Event
from locations.models import Location
from django.db.models import Q


def global_search(request):
    query = request.GET.get('q', '')

    characters = []
    houses = []
    events = []
    locations = []

    if query:
        characters = Character.objects.filter(
            Q(name__icontains=query) |
            Q(title__icontains=query)
        )

        houses = House.objects.filter(
            Q(name__icontains=query) |
            Q(words__icontains=query)
        )

        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        locations = Location.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'query': query,
        'characters': characters,
        'houses': houses,
        'events': events,
        'locations': locations
    }

    return render(request, 'search_results.html', context)
