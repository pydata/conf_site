from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from conf_site.reviews.views import (
    ProposalDetailView,
    ProposalFeedbackPostView,
    ProposalKindListView,
    ProposalListView,
    ProposalVotePostView,
)
from conf_site.reviews.views.export import ExportReviewersView
from conf_site.reviews.views.keywords import (
    ReviewKeywordDetailView,
    ReviewKeywordListView,
)
from conf_site.reviews.views.results import (
    ProposalChangeResultPostView,
    ProposalResultListView,
    ProposalMultieditPostView,
)

urlpatterns = [
    path(
        "edit/", ProposalMultieditPostView.as_view(), name="review_multiedit"
    ),
    path(
        "keyword/", ReviewKeywordListView.as_view(), name="review_keyword_list"
    ),
    path(
        "keyword/<slug:keyword_slug>/",
        ReviewKeywordDetailView.as_view(),
        name="review_keyword_detail",
    ),
    path(
        "kind/<kind>/",
        ProposalKindListView.as_view(),
        name="review_proposal_kind_list",
    ),
    path(
        "proposal/<int:pk>/",
        ProposalDetailView.as_view(),
        name="review_proposal_detail",
    ),
    path(
        "proposal/<int:pk>/feedback/",
        ProposalFeedbackPostView.as_view(),
        name="review_proposal_feedback",
    ),
    path(
        "proposal/<int:pk>/result/<status>/",
        ProposalChangeResultPostView.as_view(),
        name="review_proposal_change_result",
    ),
    path(
        "proposal/<int:pk>/vote/",
        ProposalVotePostView.as_view(),
        name="review_proposal_vote",
    ),
    path(
        "result/<status>/",
        ProposalResultListView.as_view(),
        name="review_proposal_result_list",
    ),
    path(
        "reviewers/export/",
        staff_member_required(ExportReviewersView.as_view()),
        name="reviewer_export",
    ),
    path("", ProposalListView.as_view(), name="review_proposal_list"),
]
