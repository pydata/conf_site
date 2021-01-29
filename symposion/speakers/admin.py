from __future__ import unicode_literals
from django.contrib import admin

from symposion.speakers.models import Speaker


admin.site.register(
    Speaker,
    list_display=[
        "name",
        "slug",
        "email",
        "speaker_timezone",
        "github_username",
        "twitter_username",
        "created",
    ],
    prepopulated_fields={"slug": ("name",)},
    search_fields=["name", "user__email"],
)
