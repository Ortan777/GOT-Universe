from django.shortcuts import render, get_object_or_404
from .models import Character
import json
from .analytics import calculate_influence
import json
from characters.analytics import calculate_influence
from houses.analytics import calculate_house_power
from .analytics import calculate_influence


def character_list(request):
    characters = Character.objects.select_related('house').all()
    return render(request, 'characters/character_list.html', {'characters': characters})


def character_detail(request, id):
    character = get_object_or_404(Character, id=id)

    children = Character.objects.filter(father=character) | Character.objects.filter(mother=character)

    context = {
        'character': character,
        'children': children.distinct()
    }

    return render(request, 'characters/character_detail.html', context)
def character_graph(request):
    season = request.GET.get("season")

    characters = Character.objects.all()

    nodes = []
    edges = []

    for char in characters:
        nodes.append({
            "data": {
                "id": str(char.id),
                "label": char.name
            }
        })

        # Family relationships (always shown)
        if char.father:
            edges.append({
                "data": {
                    "source": str(char.father.id),
                    "target": str(char.id),
                    "label": "father"
                }
            })

        if char.mother:
            edges.append({
                "data": {
                    "source": str(char.mother.id),
                    "target": str(char.id),
                    "label": "mother"
                }
            })

        if char.spouse:
            edges.append({
                "data": {
                    "source": str(char.id),
                    "target": str(char.spouse.id),
                    "label": "spouse"
                }
            })

        # Event-based relationships filtered by season
        if season:
            events = char.events.filter(season=season)
        else:
            events = char.events.all()

        for event in events:
            for other in event.involved_characters.all():
                if other.id != char.id:
                    edges.append({
                        "data": {
                            "source": str(char.id),
                            "target": str(other.id),
                            "label": f"S{event.season}"
                        }
                    })

    graph_data = {
        "nodes": nodes,
        "edges": edges
    }

    seasons = Character.objects.values_list(
        "events__season", flat=True
    ).distinct().order_by("events__season")

    return render(request, 'characters/character_graph.html', {
        "graph_data": json.dumps(graph_data),
        "selected_season": season,
        "seasons": seasons
    })

def character_ranking(request):
    scores = calculate_influence()

    characters = Character.objects.all()

    ranked = sorted(
        characters,
        key=lambda c: scores.get(c.id, 0),
        reverse=True
    )

    # Attach score to each character
    for char in ranked:
        char.influence_value = scores.get(char.id, 0)

    return render(request, 'characters/character_ranking.html', {
        "ranked": ranked
    })

def compare_characters(request):
    characters = Character.objects.all()
    char1 = None
    char2 = None
    scores = calculate_influence()

    if request.GET.get("char1") and request.GET.get("char2"):
        char1 = Character.objects.get(id=request.GET.get("char1"))
        char2 = Character.objects.get(id=request.GET.get("char2"))

        char1.influence_value = scores.get(char1.id, 0)
        char2.influence_value = scores.get(char2.id, 0)

        char1.event_count = char1.events.count()
        char2.event_count = char2.events.count()

        char1.children_count = (
            char1.children_from_father.count() +
            char1.children_from_mother.count()
        )

        char2.children_count = (
            char2.children_from_father.count() +
            char2.children_from_mother.count()
        )

    return render(request, "characters/compare.html", {
        "characters": characters,
        "char1": char1,
        "char2": char2,
    })