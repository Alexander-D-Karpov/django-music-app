from django.contrib import admin

# Register your models here.
from music.models import Song, Room

admin.site.register(Song)
admin.site.register(Room)
