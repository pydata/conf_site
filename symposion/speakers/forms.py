from __future__ import unicode_literals
from django import forms

from symposion.speakers.models import Speaker


class SpeakerForm(forms.ModelForm):
    required_css_class = "formfield-required"

    class Meta:
        model = Speaker
        fields = [
            "name",
            "biography",
            "speaker_timezone",
            "photo",
            "github_username",
            "twitter_username",
        ]

    def clean_twitter_username(self):
        value = self.cleaned_data["twitter_username"]
        if value.startswith("@"):
            value = value[1:]
        return value
