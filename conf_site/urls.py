from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

from account.views import SignupView
try:
    import debug_toolbar
except ImportError:
    pass
import symposion.views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from cms.views import LoginEmailView
from speakers.views import ExportAcceptedSpeakerEmailView


WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"

if settings.DEBUG:
    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls)), ]
else:
    urlpatterns = []
urlpatterns += [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/login/$", LoginEmailView.as_view(), name="account_login"),
    url(r"^account/", include("account.urls")),
    url(r"^api/", include("conf_site.api.urls")),
    url(r"^cms/", include(wagtailadmin_urls)),
    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^speaker/export/$",
        staff_member_required(ExportAcceptedSpeakerEmailView.as_view()),
        name="speaker_email_export"),
    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),
    url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^teams/", include("symposion.teams.urls")),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^schedule/", include("symposion.schedule.urls")),
    url(r"^markitup/", include("markitup.urls")),
    url(r"", include(wagtail_urls)),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
