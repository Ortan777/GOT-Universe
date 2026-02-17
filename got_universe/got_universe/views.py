import json
from django.shortcuts import render

from characters.analytics import calculate_influence
from houses.analytics import calculate_house_power

from characters.models import Character
from houses.models import House
from events.models import Event
from locations.models import Location


# 🏠 Home Dashboard
def home(request):
    # Character influence
    char_scores = calculate_influence()
    characters = Character.objects.all()

    most_influential_character = None
    if characters.exists():
        most_influential_character = max(
            characters,
            key=lambda c: char_scores.get(c.id, 0)
        )

    # House power
    house_scores = calculate_house_power()
    houses = House.objects.all()

    most_powerful_house = None
    if houses.exists():
        most_powerful_house = max(
            houses,
            key=lambda h: house_scores.get(h.id, 0)
        )

    context = {
        "most_influential_character": most_influential_character,
        "most_powerful_house": most_powerful_house,
        "total_characters": Character.objects.count(),
        "total_houses": House.objects.count(),
        "total_events": Event.objects.count(),
        "total_locations": Location.objects.count(),
    }

    return render(request, "home.html", context)


# 📊 Analytics Dashboard (Charts)
def analytics_dashboard(request):
    # Character influence data
    char_scores = calculate_influence()
    characters = Character.objects.all()

    char_data = []
    for char in characters:
        char_data.append({
            "name": char.name,
            "score": char_scores.get(char.id, 0)
        })

    # Top 5 characters
    char_data = sorted(
        char_data,
        key=lambda x: x["score"],
        reverse=True
    )[:5]

    # House power data
    house_scores = calculate_house_power()
    houses = House.objects.all()

    house_data = []
    for house in houses:
        house_data.append({
            "name": house.name,
            "score": house_scores.get(house.id, 0)
        })

    house_data = sorted(
        house_data,
        key=lambda x: x["score"],
        reverse=True
    )

    context = {
        "char_data": json.dumps(char_data),
        "house_data": json.dumps(house_data),
    }

    return render(request, "analytics_dashboard.html", context)
