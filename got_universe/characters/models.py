from django.db import models
from houses.models import House


class Character(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    house = models.ForeignKey(
        House,
        on_delete=models.SET_NULL,
        null=True,
        related_name='members'
    )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    title = models.CharField(max_length=200, blank=True, null=True)

    father = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children_from_father'
    )

    mother = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children_from_mother'
    )

    spouse = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner'
    )

    is_alive = models.BooleanField(default=True)
    birth_year = models.IntegerField(blank=True, null=True)
    death_year = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def influence_score(self):
        events_count = self.events.count()
        children_count = self.children_from_father.count() + self.children_from_mother.count()
        spouse_bonus = 2 if self.spouse else 0

        return (events_count * 3) + (children_count * 2) + spouse_bonus
