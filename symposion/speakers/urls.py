from django.conf.urls import re_path
from .views import (
    speaker_create,
    speaker_create_token,
    speaker_edit,
    speaker_create_staff,
)

urlpatterns = [
    re_path(r"^create/$", speaker_create, name="speaker_create"),
    re_path(
        r"^create/(\w+)/$", speaker_create_token, name="speaker_create_token"
    ),
    re_path(r"^edit/(?:(?P<pk>\d+)/)?$", speaker_edit, name="speaker_edit"),
    re_path(
        r"^staff/create/(\d+)/$",
        speaker_create_staff,
        name="speaker_create_staff",
    ),
]
