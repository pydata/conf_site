from django.conf.urls import include
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from conf_site.proposals.views import (
    ExportProposalSubmittersView,
    ExportProposalsView,
    ExportSubmissionsView,
)


urlpatterns = [
    path(
        "export/",
        staff_member_required(ExportProposalsView.as_view()),
        name="proposal_export",
    ),
    path(
        "submissions/export/",
        staff_member_required(ExportSubmissionsView.as_view()),
        name="submission_export",
    ),
    path(
        "submitters/export/",
        staff_member_required(ExportProposalSubmittersView.as_view()),
        name="proposal_submitter_export",
    ),
    path("", include("symposion.proposals.urls")),
]
