import requests
import time
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from characters.models import Character
from difflib import SequenceMatcher

class Command(BaseCommand):
    help = 'Fetch character images from ThronesAPI'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fetched without saving',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of characters to process',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']
        
        self.stdout.write(self.style.SUCCESS("🌐 Fetching data from ThronesAPI..."))
        
        # Fetch all characters from API
        try:
            response = requests.get(
                "https://thronesapi.com/api/v2/Characters",
                timeout=10,
                headers={'User-Agent': 'WesterosExplorer/1.0'}
            )
            response.raise_for_status()
            api_characters = response.json()
            self.stdout.write(self.style.SUCCESS(f"✓ Found {len(api_characters)} characters in API"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Failed to fetch from API: {str(e)}"))
            return
        
        # Get all your local characters
        local_characters = Character.objects.all()
        if limit:
            local_characters = local_characters[:limit]
        
        self.stdout.write(f"\n📊 Processing {len(local_characters)} local characters...")
        
        matched = 0
        updated = 0
        failed = []
        
        for local_char in local_characters:
            self.stdout.write(f"\n  Checking: {local_char.name}")
            
            # Try to find matching character in API
            best_match = self.find_best_match(local_char.name, api_characters)
            
            if best_match:
                matched += 1
                similarity, api_char = best_match
                
                self.stdout.write(f"    ✓ Match found: {api_char['fullName']} (similarity: {similarity:.0%})")
                
                # Check if API has image
                if api_char.get('imageUrl'):
                    if not dry_run:
                        if self.save_character_image(local_char, api_char):
                            updated += 1
                            self.stdout.write(self.style.SUCCESS(f"      ✓ Image saved"))
                        else:
                            self.stdout.write(self.style.ERROR(f"      ✗ Failed to save image"))
                    else:
                        self.stdout.write(f"      [DRY RUN] Would save image from: {api_char['imageUrl']}")
                else:
                    self.stdout.write(f"      ⚠ No image URL in API")
            else:
                failed.append(local_char.name)
                self.stdout.write(self.style.WARNING(f"    ✗ No match found"))
            
            # Be nice to the API
            time.sleep(0.5)
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"✅ Complete!"))
        self.stdout.write(f"  • Characters processed: {len(local_characters)}")
        self.stdout.write(f"  • Matches found: {matched}")
        self.stdout.write(f"  • Images updated: {updated}")
        if failed:
            self.stdout.write(self.style.WARNING(f"  • No matches: {len(failed)}"))
            self.stdout.write(f"    Examples: {', '.join(failed[:5])}")
    
    def find_best_match(self, local_name, api_characters):
        """Find best matching character in API data"""
        best_match = None
        best_similarity = 0
        
        for api_char in api_characters:
            # Try different name variations
            api_names = [
                api_char.get('fullName', ''),
                api_char.get('firstName', '') + ' ' + api_char.get('lastName', ''),
                api_char.get('firstName', ''),
                api_char.get('lastName', ''),
            ]
            
            for api_name in api_names:
                if not api_name:
                    continue
                
                # Calculate similarity
                similarity = SequenceMatcher(None, local_name.lower(), api_name.lower()).ratio()
                
                # Check if one name contains the other
                if local_name.lower() in api_name.lower() or api_name.lower() in local_name.lower():
                    similarity = max(similarity, 0.8)
                
                if similarity > best_similarity and similarity > 0.6:  # Threshold
                    best_similarity = similarity
                    best_match = api_char
        
        if best_match:
            return (best_similarity, best_match)
        return None
    
    def save_character_image(self, character, api_data):
        """Save image from API to character"""
        try:
            image_url = api_data['imageUrl']
            
            # Download image
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # Create filename
                filename = f"{character.name.lower().replace(' ', '_')}.jpg"
                
                # Save to character
                character.image.save(
                    filename,
                    ContentFile(response.content),
                    save=True
                )
                return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"      Error: {str(e)}"))
        return False