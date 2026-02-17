from django.db import models
from characters.models import Character
from locations.models import Location
from houses.models import House


class Event(models.Model):

    EVENT_TYPE_CHOICES = [
        ('battle', 'Battle'),
        ('death', 'Death'),
        ('coronation', 'Coronation'),
        ('betrayal', 'Betrayal'),
        ('political', 'Political Event'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)

    season = models.IntegerField(blank=True, null=True)
    episode = models.IntegerField(blank=True, null=True)

    year = models.IntegerField(blank=True, null=True)

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )

    involved_characters = models.ManyToManyField(
        Character,
        blank=True,
        related_name='events'
    )

    involved_houses = models.ManyToManyField(
        House,
        blank=True,
        related_name='events'
    )

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
