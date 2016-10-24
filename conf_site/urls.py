from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView

from account.views import SignupView
if settings.DEBUG:
    import debug_toolbar
from django_markdown import flatpages as markdown_flatpages
import symposion.views

from misc.views import LoginEmailView
from speakers.views import ExportAcceptedSpeakerEmailView


WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"


urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),

    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/login/$", LoginEmailView.as_view(), name="account_login"),
    url(r"^account/", include("account.urls")),
    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    url(r"^speaker/export/$",
        staff_member_required(ExportAcceptedSpeakerEmailView.as_view()),
        name="speaker_email_export"),
    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),
    url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^teams/", include("symposion.teams.urls")),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^schedule/", include("symposion.schedule.urls")),
    url("^markdown/", include("django_markdown.urls")),
    url(r"^markitup/", include("markitup.urls")),

    url(r"^api/", include("conf_site.api.urls")),
]

if settings.DEBUG:
    urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls)), ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
markdown_flatpages.register()
