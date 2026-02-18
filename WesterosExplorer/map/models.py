# In your map app, create models.py
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    ruling_house = models.ForeignKey('characters.House', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    coordinates_x = models.IntegerField(help_text="X coordinate on map")
    coordinates_y = models.IntegerField(help_text="Y coordinate on map")
    image = models.ImageField(upload_to='map/locations/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('location_detail', args=[self.id])