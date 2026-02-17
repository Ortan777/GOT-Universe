from django.db import models
from django.urls import reverse

class House(models.Model):
    """Model for Great Houses"""
    name = models.CharField(max_length=100)
    sigil = models.CharField(max_length=500, help_text="Description of the sigil")
    words = models.CharField(max_length=200, blank=True)
    seat = models.CharField(max_length=200, blank=True)
    region = models.CharField(max_length=100)
    founded = models.CharField(max_length=100, blank=True, help_text="When was it founded?")
    extinct = models.CharField(max_length=100, blank=True, help_text="If extinct, when?")
    image = models.ImageField(upload_to='houses/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Houses"
    
    def __str__(self):
        return f"House {self.name}"
    
    def get_absolute_url(self):
        return reverse('house_detail', args=[self.id])

class Character(models.Model):
    """Model for characters"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    ]
    
    name = models.CharField(max_length=100)
    also_known_as = models.JSONField(default=list, blank=True, help_text="Other names/titles")
    
    # House relations
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    
    # Family relations
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_father')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children_mother')
    spouse = models.ManyToManyField('self', blank=True, symmetrical=True)
    
    # Life details
    born = models.CharField(max_length=100, blank=True, help_text="e.g., '283 AC' or 'In 273 AC at Dragonstone'")
    died = models.CharField(max_length=100, blank=True, help_text="e.g., '298 AC' or 'During the Rebellion'")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    
    # Physical attributes
    culture = models.CharField(max_length=100, blank=True)
    titles = models.JSONField(default=list, blank=True)
    
    # Dragon
    dragon = models.CharField(max_length=100, blank=True, help_text="Name of dragon if rider")
    
    # Media
    image = models.ImageField(upload_to='characters/', blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('character_detail', args=[self.id])
    
    def get_father_name(self):
        return self.father.name if self.father else "Unknown"
    
    def get_mother_name(self):
        return self.mother.name if self.mother else "Unknown"
    
    def get_spouses(self):
        return ", ".join([spouse.name for spouse in self.spouse.all()]) or "None"