from django.db import models
from django.urls import reverse
from django.db.models import Q

class House(models.Model):
    """Model for Great Houses"""
    name = models.CharField(max_length=100)
    sigil = models.CharField(max_length=500, blank=True, help_text="Description of the sigil")
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
    
    def member_count(self):
        return Character.objects.filter(house=self).count()

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
    image_url = models.URLField(blank=True, null=True, help_text="External image URL (from APIs)")
    thumbnail = models.ImageField(upload_to='characters/thumbnails/', blank=True, null=True)
    
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
    
    def get_dragon_display(self):
        """Get formatted dragon info"""
        from .dragon_data import get_dragon_info
        
        if self.dragon:
            return self.dragon
        
        # Check dragon data
        dragon_info = get_dragon_info(self.name)
        if dragon_info:
            return dragon_info
        
        # Check if Targaryen in dragon era
        if self.house and self.house.name == 'Targaryen':
            if self.born:
                born_str = str(self.born)
                if 'BC' in born_str or ('AC' in born_str and int(born_str.split()[0]) < 150):
                    return "Dragon rider (specific dragon unknown)"
        
        return None
    
    def is_dragon_rider(self):
        """Check if character rides a dragon"""
        from .dragon_data import is_dragon_rider
        return is_dragon_rider(self)