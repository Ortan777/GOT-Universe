from django.contrib import admin
from .models import Character
from events.models import Event


class EventInline(admin.TabularInline):
    model = Event.involved_characters.through
    extra = 0
    verbose_name = "Event"
    verbose_name_plural = "Events"


class ChildFromFatherInline(admin.TabularInline):
    model = Character
    fk_name = 'father'
    extra = 0


class ChildFromMotherInline(admin.TabularInline):
    model = Character
    fk_name = 'mother'
    extra = 0


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'house', 'gender', 'is_alive')
    list_filter = ('house', 'gender', 'is_alive')
    search_fields = ('name',)
    inlines = [ChildFromFatherInline, ChildFromMotherInline, EventInline]
