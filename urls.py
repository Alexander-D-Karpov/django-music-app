from django.urls import path

from .views import *

urlpatterns = [
    path("", player, name="music"),
    path("song/<str:slug>", song, name="song_share"),
    path("upload", upload, name="music_upload"),
    path("listen", listen_tracker, name="listen_tracker"),
    path("room", room_select, name="rooms"),
    path("<str:slug>", room, name="room"),
]
