# -*- coding: utf-8 -*-
# Views relating to accepting/rejecting a reviewed proposal.
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from conf_site.proposals.models import Proposal
from conf_site.reviews.models import ProposalResult
from conf_site.reviews.views import ProposalListView


class SuperuserOnlyView(UserPassesTestMixin, View):
    """A view which only allows access to superusers."""

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif not self.request.user.is_anonymous:
            # Non-anonymous, non-superuser users should see an error page.
            self.raise_exception = True
        return False


class ProposalChangeResultPostView(SuperuserOnlyView):
    """A view to allow superusers to change a proposal's voting result."""

    http_method_names = ["get"]

    def get(self, *args, **kwargs):
        """Update an individual ProposalResult object."""
        proposal = Proposal.objects.get(pk=kwargs["pk"])
        result = ProposalResult.objects.get_or_create(proposal=proposal)[0]
        result.status = kwargs["status"]
        result.save()

        return HttpResponseRedirect(
            reverse("review_proposal_detail", args=[proposal.id])
        )


class ProposalResultListView(SuperuserOnlyView, ProposalListView):

    def get(self, request, *args, **kwargs):
        self.status = kwargs["status"]
        return super(ProposalResultListView, self).get(
            request, *args, **kwargs
        )

    def get_queryset(self):
        return Proposal.objects.order_by("pk").filter(
            review_result__status=self.status
        )

    def get_context_data(self, **kwargs):
        context = super(ProposalResultListView, self).get_context_data(
            **kwargs
        )
        temp_result = ProposalResult(status=self.status)
        context["proposal_category"] = temp_result.get_status_display()
        return context
