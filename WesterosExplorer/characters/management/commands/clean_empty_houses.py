from django.core.management.base import BaseCommand
from characters.models import House, Character

class Command(BaseCommand):
    help = 'Find and optionally delete houses with no characters'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete empty houses',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List empty houses without deleting',
        )
    
    def handle(self, *args, **options):
        empty_houses = []
        all_houses = House.objects.all().order_by('name')
        
        for house in all_houses:
            member_count = Character.objects.filter(house=house).count()
            if member_count == 0:
                empty_houses.append(house)
        
        if options['list']:
            self.stdout.write(self.style.SUCCESS(f"\nFound {len(empty_houses)} empty houses:\n"))
            for house in empty_houses:
                self.stdout.write(f"  • {house.name} (ID: {house.id})")
        
        elif options['delete']:
            self.stdout.write(self.style.WARNING(f"\nDeleting {len(empty_houses)} empty houses...\n"))
            for house in empty_houses:
                house.delete()
                self.stdout.write(f"  ✗ Deleted: {house.name}")
            self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully deleted {len(empty_houses)} empty houses"))
        
        else:
            self.stdout.write(self.style.WARNING(f"\nFound {len(empty_houses)} empty houses"))
            self.stdout.write("Use --list to see them or --delete to remove them")