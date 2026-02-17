from django.shortcuts import render
from .models import House
from django.shortcuts import get_object_or_404
from .analytics import calculate_house_power
import json
from characters.models import Character
from events.models import Event

def house_list(request):
    houses = House.objects.all()
    return render(request, 'houses/house_list.html', {'houses': houses})

def house_detail(request, id):
    house = get_object_or_404(House, id=id)
    return render(request, 'houses/house_detail.html', {'house': house})

def house_ranking(request):
    house_scores = calculate_house_power()
    houses = House.objects.all()

    ranked = sorted(
        houses,
        key=lambda h: house_scores.get(h.id, 0),
        reverse=True
    )

    for house in ranked:
        house.power_score = house_scores.get(house.id, 0)

    return render(request, 'houses/house_ranking.html', {
        "ranked": ranked
    })

def house_network(request):
    houses = House.objects.all()

    nodes = []
    edges = []

    # Create nodes
    for house in houses:
        nodes.append({
            "data": {
                "id": str(house.id),
                "label": house.name
            }
        })

    # Marriage alliances
    characters = Character.objects.exclude(spouse=None)

    for char in characters:
        if char.spouse and char.house and char.spouse.house:
            if char.house.id != char.spouse.house.id:
                edges.append({
                    "data": {
                        "source": str(char.house.id),
                        "target": str(char.spouse.house.id),
                        "label": "Marriage"
                    }
                })

    # Shared event alliances
    events = Event.objects.all()

    for event in events:
        involved_houses = list(event.involved_houses.all())

        for i in range(len(involved_houses)):
            for j in range(i + 1, len(involved_houses)):
                edges.append({
                    "data": {
                        "source": str(involved_houses[i].id),
                        "target": str(involved_houses[j].id),
                        "label": "Event"
                    }
                })

    graph_data = {
        "nodes": nodes,
        "edges": edges
    }

    return render(request, "houses/house_network.html", {
        "graph_data": json.dumps(graph_data)
    })