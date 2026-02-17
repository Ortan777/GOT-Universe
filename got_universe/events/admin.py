from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'season', 'location')
    list_filter = ('event_type', 'season')
    search_fields = ('title',)
    filter_horizontal = ('involved_characters', 'involved_houses')
