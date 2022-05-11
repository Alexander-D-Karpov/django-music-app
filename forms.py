from django import forms

from music.models import Song


class FileForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["track"]
        widgets = {
            "track": forms.FileInput(
                attrs={
                    "type": "file",
                    "class": "form-control",
                    "id": "file",
                    "aria-describedby": "basic-addon3",
                    "name": "file",
                    "multiple": "true",
                }
            )
        }
