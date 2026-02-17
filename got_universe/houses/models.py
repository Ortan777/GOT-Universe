from django.db import models

class House(models.Model):
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
    words = models.CharField(max_length=200)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    seat = models.CharField(max_length=100)
    founder = models.CharField(max_length=100, blank=True, null=True)
    sigil_description = models.TextField(blank=True, null=True)
    is_extinct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
