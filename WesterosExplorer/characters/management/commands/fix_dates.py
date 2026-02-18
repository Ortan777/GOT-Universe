from django.core.management.base import BaseCommand
from characters.models import Character  # This should now work
import re

class Command(BaseCommand):
    help = 'Fix improperly formatted dates in the database'
    
    def format_got_date(self, date_string):
        """Format Game of Thrones dates properly"""
        if not date_string:
            return date_string
        
        date_string = str(date_string).strip()
        
        # Remove any duplicate AC/BC
        if "AC AC" in date_string:
            date_string = date_string.replace("AC AC", "AC")
        if "BC BC" in date_string:
            date_string = date_string.replace("BC BC", "BC")
        if "AC BC" in date_string or "BC AC" in date_string:
            # This is invalid, take the first part
            parts = date_string.split()
            if len(parts) >= 2:
                date_string = f"{parts[0]} {parts[1]}"
        
        # Ensure proper spacing
        if "AC" in date_string and "AC" not in date_string.split()[-1]:
            date_string = date_string.replace("AC", " AC").strip()
        if "BC" in date_string and "BC" not in date_string.split()[-1]:
            date_string = date_string.replace("BC", " BC").strip()
        
        # Handle numeric only (assume AC)
        if date_string.isdigit():
            return f"{date_string} AC"
        
        return date_string
    
    def handle(self, *args, **options):
        try:
            characters = Character.objects.all()
            fixed_count = 0
            
            self.stdout.write(self.style.SUCCESS(f"Found {characters.count()} characters to check..."))
            
            for character in characters:
                changed = False
                
                # Fix born date
                if character.born:
                    new_born = self.format_got_date(character.born)
                    if new_born != character.born:
                        self.stdout.write(f"  Fixing {character.name} born: '{character.born}' -> '{new_born}'")
                        character.born = new_born
                        changed = True
                
                # Fix died date
                if character.died:
                    new_died = self.format_got_date(character.died)
                    if new_died != character.died:
                        self.stdout.write(f"  Fixing {character.name} died: '{character.died}' -> '{new_died}'")
                        character.died = new_died
                        changed = True
                
                if changed:
                    character.save()
                    fixed_count += 1
            
            self.stdout.write(self.style.SUCCESS(f"\n✓ Fixed dates for {fixed_count} characters"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))