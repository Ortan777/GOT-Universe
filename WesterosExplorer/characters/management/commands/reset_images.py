from django.core.management.base import BaseCommand
from characters.models import Character
import os

class Command(BaseCommand):
    help = 'Reset all character images and replace with house banners/placeholders'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Get all characters with images
        characters_with_images = Character.objects.exclude(image='')
        
        self.stdout.write(f"Found {characters_with_images.count()} characters with images")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("\nDRY RUN - No changes will be made\n"))
            for char in characters_with_images:
                self.stdout.write(f"  Would delete: {char.name} - {char.image}")
        else:
            # Actually delete the images
            deleted_count = 0
            for char in characters_with_images:
                if char.image:
                    # Delete the file from storage
                    if char.image.storage.exists(char.image.name):
                        char.image.storage.delete(char.image.name)
                        self.stdout.write(f"  ✗ Deleted image for: {char.name}")
                    # Clear the field
                    char.image = None
                    char.save()
                    deleted_count += 1
            
            self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully removed {deleted_count} images"))