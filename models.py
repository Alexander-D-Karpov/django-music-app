import os
import secrets
import string

from django.db import models
from django.urls import reverse

from site_blog import settings
from user.models import Person


class Room(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=10)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)

    def get_songs_count(self):
        return len(RoomTrack.objects.filter(room__slug=self.slug))


class Song(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.CharField(max_length=100, blank=True)
    track = models.FileField(upload_to="uploads/music/", blank=False)
    image = models.ImageField(upload_to="uploads/images/")
    artist = models.CharField(max_length=100, blank=True)
    album = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    time_played = models.IntegerField(default=0)

    def gen_song(self, *args, **kwargs):
        super(Song, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "".join(secrets.choice(string.ascii_letters) for _ in range(10))
        path = "/var/www/media/"
        if settings.DEBUG:
            path = "/home/sanspie/PycharmProjects/site_blog/media/"
        self.image = f"/uploads/images/{self.slug}.jpg"
        os.system(f"ffmpeg -i {self.track.path} {path}/uploads/images/{self.slug}.jpg")
        super(Song, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = "".join(secrets.choice(string.ascii_letters) for _ in range(10))

        super(Song, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("song_share", kwargs={"slug": self.slug})


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(Person, on_delete=models.CASCADE)
    length = models.IntegerField(default=0)

    def add_song(self, song: Song):
        self.length += 1
        SongInPlaylist.objects.create(self, song)
        super(Playlist, self).save(update_fields=["length"])

    def remove_song(self, song: Song):
        if song := SongInPlaylist.objects.filter(self, song):
            song[0].remove()
            self.length -= 1
            super(Playlist, self).save(update_fields=["length"])


class SongInPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class RoomTrack(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    track = models.ForeignKey(Song, on_delete=models.CASCADE)
