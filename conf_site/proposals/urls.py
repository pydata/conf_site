from django.conf.urls import include
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from conf_site.proposals.views import ExportProposalSubmittersView


urlpatterns = [
    path(
        "submitters/export/",
        staff_member_required(ExportProposalSubmittersView.as_view()),
        name="proposal_submitter_export",
    ),
    path("", include("symposion.proposals.urls")),
]
