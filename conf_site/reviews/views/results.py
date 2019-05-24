# -*- coding: utf-8 -*-
# Views relating to accepting/rejecting a reviewed proposal.
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.template.defaultfilters import pluralize
from django.urls import reverse
from django.views.generic import View

from conf_site.proposals.models import Proposal
from conf_site.reviews.models import ProposalNotification, ProposalResult
from conf_site.reviews.views import ProposalListView
from symposion.schedule.models import Presentation


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
        if self.status == ProposalResult.RESULT_UNDECIDED:
            # Create ProposalResults for proposals that do not have them.
            proposals_without_result = Proposal.objects.filter(
                review_result=None
            )
            for proposal in proposals_without_result:
                ProposalResult.objects.create(
                    proposal=proposal, status=ProposalResult.RESULT_UNDECIDED
                )
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


class ProposalMultieditPostView(SuperuserOnlyView):
    """A view to let superusers modify multiple proposals' results."""

    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        proposal_pks = self.request.POST.getlist("proposal_pk")
        proposals = Proposal.objects.filter(pk__in=proposal_pks)
        new_status = self.request.POST.get("mark_status")
        if new_status:
            # <queryset>.update() will not work here because
            # the status field lives in the related model
            # ProposalResult.
            for proposal in proposals:
                try:
                    proposal.review_result.status = new_status
                    proposal.review_result.save()
                except AttributeError:
                    proposal.review_result = ProposalResult.objects.create(
                        proposal=proposal, status=new_status
                    )
            return HttpResponseRedirect(
                reverse("review_proposal_result_list", args=[new_status])
            )
        elif self.request.POST.get("send_notification"):
            # Save ProposalNotification to database, as a type
            # of rudimentary logging.
            notification = ProposalNotification.objects.create(
                from_address=self.request.POST.get("from_address"),
                subject=self.request.POST.get("subject"),
                body=self.request.POST.get("body"),
            )
            notification.proposals.set(proposals)
            notification.send_email()
            return HttpResponseRedirect(reverse("review_proposal_list"))
        elif self.request.POST.get("create_presentations"):
            num_presentations_created = 0
            for proposal in proposals:
                # We don't need to add all of the proposal's metadata
                # to the presentation. Title, description, etc.
                # will be added when we save the proposal.
                # See https://github.com/pydata/conf_site/pull/176.
                presentation, created = Presentation.objects.get_or_create(
                    proposal_base=proposal.proposalbase_ptr,
                    section=proposal.section,
                    speaker=proposal.speaker,
                )
                # If the presentation already existed, we do not need
                # to attach it to the proposal.
                if created:
                    proposal.presentation = presentation
                    proposal.save()
                    num_presentations_created += 1
            # Create a message if any new presentations were created.
            if num_presentations_created:
                messages.success(
                    self.request,
                    "{} presentation{} created.".format(
                        num_presentations_created,
                        pluralize(num_presentations_created),
                    ),
                )
            else:
                messages.warning(
                    self.request,
                    "All selected proposals already had presentations.",
                )
            # Since the "create presentations" action can only
            # be initated from the "Accepted Proposals"
            # category listing, we return the user there.
            return HttpResponseRedirect(
                reverse(
                    "review_proposal_result_list",
                    args=[ProposalResult.RESULT_ACCEPTED],
                )
            )
