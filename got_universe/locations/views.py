from django.shortcuts import render, get_object_or_404
from .models import Location
from django.core.serializers import serialize
import json
from houses.analytics import calculate_house_power
from houses.models import House



def location_list(request):
    locations = Location.objects.all()
    return render(request, 'locations/location_list.html', {'locations': locations})


def location_detail(request, id):
    location = get_object_or_404(Location, id=id)

    events = location.events.all()

    context = {
        'location': location,
        'events': events
    }

    return render(request, 'locations/location_detail.html', context)

def map_view(request):
    house_scores = calculate_house_power()
    locations = Location.objects.exclude(latitude__isnull=True)

    max_power = max(house_scores.values()) if house_scores else 1

    data = []

    for loc in locations:
        house = House.objects.filter(seat=loc.name).first()

        power = 0
        if house:
            power = house_scores.get(house.id, 0)

        normalized = power / max_power if max_power else 0

        data.append({
            "id": loc.id,
            "name": loc.name,
            "lat": loc.latitude,
            "lng": loc.longitude,
            "power": normalized
        })

    return render(request, 'locations/map.html', {
        "locations_json": json.dumps(data)
    })