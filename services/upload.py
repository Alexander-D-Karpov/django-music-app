import os
import tempfile
from io import BytesIO
from pprint import pprint

from PIL.Image import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

import eyed3
from django.core.files import File
from django.utils.text import slugify
from pydub import AudioSegment
from deep_translator import GoogleTranslator

from common.generator import gen_slug
from music.models import Song


def _convert_track(file_location: str, temp_location: str) -> bool:
    flac_audio = AudioSegment.from_file(file_location, file_location.split(".")[-1])
    flac_audio.export(temp_location, format="mp3")
    return os.path.isfile(temp_location)


def _parse_track(file_location: str, file_name: str) -> dict:
    data = {}
    audio = eyed3.load(file_location)
    if audio.tag.title:
        data["name"] = audio.tag.title
    else:
        data["name"] = file_name

    slug = slugify(GoogleTranslator(source='auto', target='en').translate(data["name"]))
    if slug:
        data["slug"] = slug
    else:
        slug = gen_slug(3)
        while not Song.objects.filter(slug=slug).exists():
            slug = gen_slug(3)
        data["slug"] = slug

    data["track"] = File(open(file_location, "r"), data["slug"] + ".mp3")
    print(data["slug"])

    return data


def prepare_track(file_location: str, file_name: str):
    if not os.path.isfile(file_location):
        raise FileExistsError
    fp = tempfile.NamedTemporaryFile()
    if not _convert_track(file_location, fp.name):
        raise Exception
    data = _parse_track(fp.name, file_name.split(".")[0])
    fp.close()
