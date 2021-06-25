from django.conf import settings
from django.conf.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from django.views.generic.base import TemplateView

try:
    import debug_toolbar
except ImportError:
    pass
import symposion.views

from conf_site.core.views import csrf_failure, TimeZoneChangeView
from conf_site.schedule.views import (
    ExportPresentationSpeakerView,
    PresentationDetailView,
    PresentationRedirectView,
)
from conf_site.speakers.views import (
    ExportAcceptedSpeakerEmailView,
    SpeakerDetailView,
    SpeakerListView,
    SpeakerRedirectView,
)


WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"

if settings.DEBUG:
    urlpatterns = [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
else:
    urlpatterns = []
urlpatterns += [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^accounts/", include("allauth.urls")),
    re_path(r"^api/", include("conf_site.api.urls")),
    re_path(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    re_path(
        r"^speaker/export/$",
        staff_member_required(ExportAcceptedSpeakerEmailView.as_view()),
        name="speaker_email_export",
    ),
    re_path(
        r"^speaker/list/$", SpeakerListView.as_view(), name="speaker_list"
    ),
    path(
        "speaker/profile/<int:pk>/",
        SpeakerRedirectView.as_view(),
        name="speaker_profile_redirect",
    ),
    path(
        "speaker/profile/<int:pk>/<slug:slug>/",
        SpeakerDetailView.as_view(),
        name="speaker_profile",
    ),
    re_path(r"^speaker/", include("symposion.speakers.urls")),
    re_path(r"^proposals/", include("conf_site.proposals.urls")),
    re_path(r"^reviews/", include("conf_site.reviews.urls")),
    path(
        "schedule/presentation/<int:pk>/",
        PresentationRedirectView.as_view(),
        name="schedule_presentation_redirect",
    ),
    path(
        "schedule/presentation/<int:pk>/<slug:slug>/",
        PresentationDetailView.as_view(),
        name="schedule_presentation_detail",
    ),
    re_path(
        r"^schedule/presentation/export/$",
        staff_member_required(ExportPresentationSpeakerView.as_view()),
        name="presentation_speaker_export",
    ),
    re_path(r"^schedule/", include("symposion.schedule.urls")),
    re_path(
        r"^time-zone/$", TimeZoneChangeView.as_view(), name="time_zone_change"
    ),
    re_path(r"^403-csrf/", csrf_failure, name="403-csrf"),
    re_path(r"^413/", TemplateView.as_view(template_name="413.html")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
