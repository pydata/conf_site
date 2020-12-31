from django.conf.urls import re_path

from .views import (
    proposal_submit,
    proposal_submit_kind,
    proposal_detail,
    proposal_edit,
    proposal_speaker_manage,
    proposal_cancel,
    proposal_pending_join,
    proposal_pending_decline,
    document_create,
    document_delete,
    document_download,
)

urlpatterns = [
    re_path(r"^submit/$", proposal_submit, name="proposal_submit"),
    re_path(
        r"^submit/([\w\-]+)/$",
        proposal_submit_kind,
        name="proposal_submit_kind",
    ),
    re_path(r"^(\d+)/$", proposal_detail, name="proposal_detail"),
    re_path(r"^(\d+)/edit/$", proposal_edit, name="proposal_edit"),
    re_path(
        r"^(\d+)/speakers/$",
        proposal_speaker_manage,
        name="proposal_speaker_manage",
    ),
    re_path(r"^(\d+)/cancel/$", proposal_cancel, name="proposal_cancel"),
    re_path(
        r"^(\d+)/join/$", proposal_pending_join, name="proposal_pending_join"
    ),
    re_path(
        r"^(\d+)/decline/$",
        proposal_pending_decline,
        name="proposal_pending_decline",
    ),
    re_path(
        r"^(\d+)/document/create/$",
        document_create,
        name="proposal_document_create",
    ),
    re_path(
        r"^document/(\d+)/delete/$",
        document_delete,
        name="proposal_document_delete",
    ),
    re_path(
        r"^document/(\d+)/([^/]+)$",
        document_download,
        name="proposal_document_download",
    ),
]
