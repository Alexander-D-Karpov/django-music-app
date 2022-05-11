from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from .models import Song, Room
from random import shuffle
from .forms import FileForm
import eyed3

from .services.upload import prepare_track


def player(request):
    playlist = [x for x in Song.objects.all()]
    shuffle(playlist)
    return render(request, "music/index.html", context={"playlist": playlist})


def song(request, slug):
    sng = get_object_or_404(Song, slug=slug)
    sng.time_played += 1
    sng.save(update_fields=["time_played"])
    return render(request, "music/index.html", context={"playlist": [sng, sng]})


def room_select(request):
    rooms = Room.objects.all()
    return render(request, "music/rooms.html", context={"rooms": rooms})


def room(request, slug):
    data = Room.objects.get(slug=slug)
    return render(request, "music/room.html", context={"room": data})


def upload(request):
    if request.method == "POST":
        if request.user.is_superuser:
            for f in request.FILES.getlist("track"):
                print(prepare_track(f.temporary_file_path(), f.name))
    return render(request, "music/upload.html", context={"form": FileForm})


@csrf_exempt
def listen_tracker(request):
    if request.method == "POST":
        track = Song.objects.get(name=request.POST["track"])
        track.time_played = F("time_played") + 1
        track.save(update_fields=["time_played"])
        return JsonResponse(
            {"played": Song.objects.get(name=request.POST["track"]).time_played}
        )
