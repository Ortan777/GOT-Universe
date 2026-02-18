from django.core.management.base import BaseCommand
from characters.models import Character
from characters.image_utils import (
    get_character_image_url, 
    get_house_sigil_url,
    generate_placeholder
)
import requests
from django.core.files.base import ContentFile
import time
from PIL import Image
import io

class Command(BaseCommand):
    help = 'Fetch character images from online sources'
    
    def add_arguments(self, parser):
        parser.add_argument('--character', type=str, help='Specific character name to fetch')
        parser.add_argument('--house', type=str, help='Fetch all characters from a house')
        parser.add_argument('--all', action='store_true', help='Fetch all characters')
        parser.add_argument('--placeholders', action='store_true', help='Generate placeholders only')
    
    def handle(self, *args, **options):
        if options['placeholders']:
            self.generate_all_placeholders()
            return
            
        if options['all']:
            characters = Character.objects.all()
        elif options['character']:
            characters = Character.objects.filter(name__icontains=options['character'])
        elif options['house']:
            characters = Character.objects.filter(house__name__icontains=options['house'])
        else:
            self.stdout.write(self.style.WARNING('Please specify --all, --character, --house, or --placeholders'))
            return
        
        self.stdout.write(f"Fetching images for {characters.count()} characters...")
        
        success_count = 0
        fail_count = 0
        placeholder_count = 0
        
        for character in characters:
            if character.image and character.image.name:
                self.stdout.write(f"✓ {character.name} already has image")
                continue
                
            result = self.fetch_character_image(character)
            if result == 'success':
                success_count += 1
            elif result == 'placeholder':
                placeholder_count += 1
            else:
                fail_count += 1
            
            time.sleep(0.5)  # Be nice to servers
        
        self.stdout.write(self.style.SUCCESS(f"\nDone! Success: {success_count}, Placeholders: {placeholder_count}, Failed: {fail_count}"))
    
    def fetch_character_image(self, character):
        """Fetch image for a single character"""
        
        # Try to get character image URL
        image_url = get_character_image_url(character.name)
        
        if image_url:
            try:
                self.stdout.write(f"Fetching {character.name}...")
                
                # Add user agent to avoid blocking
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(image_url, timeout=10, headers=headers)
                
                if response.status_code == 200:
                    # Check if it's actually an image
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        # Create filename
                        filename = f"{character.name.lower().replace(' ', '_')}.jpg"
                        
                        # Save image
                        character.image.save(
                            filename,
                            ContentFile(response.content),
                            save=True
                        )
                        
                        self.stdout.write(self.style.SUCCESS(f"✓ Saved image for {character.name}"))
                        return 'success'
                    else:
                        self.stdout.write(self.style.WARNING(f"Not an image for {character.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Failed to fetch {character.name} (HTTP {response.status_code})"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error for {character.name}: {str(e)}"))
        
        # If no image URL or fetch failed, try house sigil
        if character.house and not character.image:
            sigil_url = get_house_sigil_url(character.house.name)
            if sigil_url:
                try:
                    response = requests.get(sigil_url, timeout=10)
                    if response.status_code == 200:
                        filename = f"{character.name.lower().replace(' ', '_')}_sigil.jpg"
                        character.image.save(
                            filename,
                            ContentFile(response.content),
                            save=True
                        )
                        self.stdout.write(self.style.SUCCESS(f"✓ Saved sigil for {character.name}"))
                        return 'success'
                except:
                    pass
        
        # If all else fails, generate placeholder
        return self.generate_placeholder(character)
    
    def generate_placeholder(self, character):
        """Generate a placeholder image for character"""
        try:
            self.stdout.write(f"Generating placeholder for {character.name}...")
            
            # Generate placeholder
            placeholder_content = generate_placeholder(character)
            
            # Save
            filename = f"{character.name.lower().replace(' ', '_')}_placeholder.jpg"
            character.image.save(
                filename,
                placeholder_content,
                save=True
            )
            
            self.stdout.write(self.style.SUCCESS(f"✓ Generated placeholder for {character.name}"))
            return 'placeholder'
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to generate placeholder for {character.name}: {str(e)}"))
            return 'fail'
    
    def generate_all_placeholders(self):
        """Generate placeholders for all characters without images"""
        characters = Character.objects.filter(image='')
        self.stdout.write(f"Generating placeholders for {characters.count()} characters...")
        
        for character in characters:
            self.generate_placeholder(character)