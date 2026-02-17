from django.db import models


class Location(models.Model):
    REGION_CHOICES = [
        ('north', 'The North'),
        ('westerlands', 'The Westerlands'),
        ('reach', 'The Reach'),
        ('stormlands', 'The Stormlands'),
        ('dorne', 'Dorne'),
        ('vale', 'The Vale'),
        ('iron_islands', 'Iron Islands'),
        ('crownlands', 'Crownlands'),
        ('essos', 'Essos'),
    ]

    name = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    description = models.TextField(blank=True, null=True)

    # These will be used later for map coordinates
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
