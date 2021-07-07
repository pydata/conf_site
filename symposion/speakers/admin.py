from __future__ import unicode_literals
from django.contrib import admin

from symposion.speakers.models import Speaker


admin.site.register(
    Speaker,
    list_display=[
        "name",
        "slug",
        "email",
        "time_zone",
        "created",
        "github_username",
        "twitter_username",
    ],
    list_filter=["time_zone"],
    prepopulated_fields={"slug": ("name",)},
    search_fields=["name"],
)
