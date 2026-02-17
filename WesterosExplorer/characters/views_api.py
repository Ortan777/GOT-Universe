from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Character, House
import json

def family_tree_data(request):
    """API endpoint to get family tree data"""
    
    # Get all characters with their relationships
    characters = Character.objects.all().select_related('house', 'father', 'mother')
    
    nodes = []
    links = []
    
    # Create nodes
    for char in characters:
        node = {
            'id': char.id,
            'name': char.name,
            'house': char.house.id if char.house else None,
            'house_name': char.house.name if char.house else 'Unknown',
            'born': char.born,
            'died': char.died,
            'gender': char.gender,
            'culture': char.culture,
            'titles': char.titles,
            'dragon': char.dragon,
            'also_known_as': char.also_known_as,
        }
        nodes.append(node)
    
    # Create links for parent-child relationships
    for char in characters:
        if char.father:
            links.append({
                'source': char.father.id,
                'target': char.id,
                'type': 'parent'
            })
        if char.mother:
            links.append({
                'source': char.mother.id,
                'target': char.id,
                'type': 'parent'
            })
    
    # Add marriage links
    for char in characters:
        for spouse in char.spouse.all():
            # Add only once (avoid duplicates)
            if char.id < spouse.id:
                links.append({
                    'source': char.id,
                    'target': spouse.id,
                    'type': 'marriage'
                })
    
    # Add sibling relationships
    characters_list = list(characters)
    for i, char1 in enumerate(characters_list):
        for char2 in characters_list[i+1:]:
            # Check if they share a parent
            if (char1.father and char2.father and char1.father.id == char2.father.id) or \
               (char1.mother and char2.mother and char1.mother.id == char2.mother.id):
                links.append({
                    'source': char1.id,
                    'target': char2.id,
                    'type': 'sibling'
                })
    
    return JsonResponse({
        'nodes': nodes,
        'links': links
    })

def house_list_api(request):
    """API endpoint to get houses with member counts"""
    houses = House.objects.all()
    data = []
    for house in houses:
        data.append({
            'id': house.id,
            'name': house.name,
            'words': house.words,
            'seat': house.seat,
            'region': house.region,
            'member_count': Character.objects.filter(house=house).count(),
            'sigil': house.sigil,
        })
    return JsonResponse(data, safe=False)

def character_detail_api(request, character_id):
    """API endpoint to get detailed character info"""
    try:
        char = Character.objects.get(id=character_id)
        
        # Get family members
        father = char.father.name if char.father else None
        mother = char.mother.name if char.mother else None
        spouses = [s.name for s in char.spouse.all()]
        
        # Get children
        children = Character.objects.filter(
            Q(father=char) | Q(mother=char)
        ).values_list('name', flat=True)
        
        # Get siblings
        siblings = []
        if char.father:
            siblings.extend(Character.objects.filter(
                father=char.father
            ).exclude(id=char.id).values_list('name', flat=True))
        if char.mother:
            siblings.extend(Character.objects.filter(
                mother=char.mother
            ).exclude(id=char.id).values_list('name', flat=True))
        
        data = {
            'id': char.id,
            'name': char.name,
            'also_known_as': char.also_known_as,
            'house': char.house.name if char.house else None,
            'born': char.born,
            'died': char.died,
            'gender': char.get_gender_display(),
            'culture': char.culture,
            'titles': char.titles,
            'dragon': char.dragon,
            'father': father,
            'mother': mother,
            'spouses': list(set(spouses)),
            'children': list(children),
            'siblings': list(set(siblings)),
        }
        return JsonResponse(data)
    except Character.DoesNotExist:
        return JsonResponse({'error': 'Character not found'}, status=404)