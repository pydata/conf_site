# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from conf_site.proposals.models import Proposal
from conf_site.reviews.forms import ProposalVoteForm, ProposalFeedbackForm
from conf_site.reviews.models import ProposalVote


class ReviewingView(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        """Check if user is in reviewers group."""
        try:
            reviewers_group = Group.objects.get(name="Reviewers")
        except Group.DoesNotExist:
            raise Exception("Reviewers user group does not exist.")
        return reviewers_group in self.request.user.groups.all()


class ProposalListView(ListView, ReviewingView):
    template_name = "reviews/proposal_list.html"

    def get_queryset(self, **kwargs):
        """Show all proposals, except those that have been cancelled."""
        return Proposal.objects.order_by("title").exclude(cancelled=True)


class ProposalDetailView(DetailView, ReviewingView):
    context_object_name = "proposal"
    model = Proposal
    template_name = "reviews/proposal_detail.html"

    def test_func(self):
        if super(ProposalDetailView, self).test_func():
            return True
        else:
            # Test whether user is one of the proposal's speakers.
            for speaker in self.get_object().speakers():
                if self.request.user == speaker.user:
                    return True
        return False

    def get_context_data(self, **kwargs):
        """Add context as to whether this is a reviewer or speaker."""
        context = super(ProposalDetailView, self).get_context_data(**kwargs)
        for speaker in self.get_object().speakers():
            if self.request.user == speaker.user:
                context["actor"] = "speaker"
            else:
                context["actor"] = "reviewer"
        context["vote_form"] = ProposalVoteForm
        context["feedback_form"] = ProposalFeedbackForm
        return context


class ProposalVotePostView(ReviewingView):
    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        """AJAX update an individual ProposalVote object."""
        proposal = Proposal.objects.get(pk=kwargs["pk"])
        vote = ProposalVote.objects.get_or_create(
            proposal=proposal,
            voter=self.request.user,
            defaults={"score": self.request.POST["score"]},
        )[0]
        vote.score = self.request.POST["score"]
        vote.comment = self.request.POST["comment"]
        vote.save()

        return HttpResponseRedirect(
            reverse("review_proposal_detail", args=[proposal.id])
        )
