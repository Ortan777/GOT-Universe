from characters.analytics import calculate_influence
from .models import House


def calculate_house_power():
    character_scores = calculate_influence()
    houses = House.objects.all()

    house_scores = {}

    for house in houses:
        total = 0
        members = house.members.all()

        for member in members:
            total += character_scores.get(member.id, 0)

        house_scores[house.id] = total

    return house_scores
