from django.core.management.base import BaseCommand
from characters.models import Character
from characters.image_utils import generate_placeholder
import requests
from django.core.files.base import ContentFile
import time

class Command(BaseCommand):
    help = 'Fetch images from all sources'
    
    def handle(self, *args, **options):
        characters = Character.objects.filter(image='')
        self.stdout.write(f"Processing {characters.count()} characters without images...")
        
        # Priority 1: ThronesAPI
        self.fetch_from_thronesapi(characters)
        
        # Priority 2: Generate placeholders for remaining
        self.generate_placeholders(characters)
    
    def fetch_from_thronesapi(self, characters):
        # Similar to previous command
        pass
    
    def generate_placeholders(self, characters):
        for character in characters:
            if not character.image:
                placeholder = generate_placeholder(character)
                filename = f"{character.id}_placeholder.jpg"
                character.image.save(filename, placeholder, save=True)
                self.stdout.write(f"Generated placeholder for {character.name}")