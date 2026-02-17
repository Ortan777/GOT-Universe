from django.contrib import admin
from .models import House
from events.models import Event


class EventInline(admin.TabularInline):
    model = Event.involved_houses.through
    extra = 0
    verbose_name = "Event"
    verbose_name_plural = "Events"


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'seat', 'is_extinct')
    list_filter = ('region', 'is_extinct')
    search_fields = ('name', 'seat')
    inlines = [EventInline]
