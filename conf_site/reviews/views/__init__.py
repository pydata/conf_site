# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from constance import config

from conf_site.proposals.models import Proposal
from conf_site.reviews.forms import (
    ProposalFeedbackForm,
    ProposalNotificationForm,
    ProposalVoteForm,
)
from conf_site.reviews.models import ProposalFeedback, ProposalVote
from symposion.proposals.models import ProposalKind
from symposion.utils.mail import send_email


def _is_reviewer_or_superuser(user):
    """Check if user is in Reviewers group or is superuser."""
    if user.is_superuser:
        return True
    # Raise an exception if the Reviewers group does not
    # exist, because this is a critical problem.
    try:
        reviewers_group = Group.objects.get(name="Reviewers")
    except Group.DoesNotExist:
        raise Exception("Reviewers user group does not exist.")
    return reviewers_group in user.groups.all()


class ReviewingView(UserPassesTestMixin, View):
    allow_speakers = False
    raise_exception = True

    def test_func(self):
        """Check if user can access reviewing section."""
        # If allow_speakers is enabled, speakers get access.
        if self.allow_speakers:
            # Test whether user is one of the proposal's speakers.
            try:
                proposal = Proposal.objects.get(pk=self.kwargs["pk"])
                for speaker in proposal.speakers():
                    if self.request.user == speaker.user:
                        return True
            except Proposal.DoesNotExist:
                pass

        return _is_reviewer_or_superuser(self.request.user)


class ProposalListView(ListView, ReviewingView):
    template_name = "reviews/proposal_list.html"

    def get_queryset(self, **kwargs):
        """Show all proposals, except those that have been cancelled."""
        return (
            Proposal.objects.order_by("pk")
            .exclude(cancelled=True)
            .select_related("kind", "speaker", "review_result")
        )

    def get_paginate_by(self, queryset):
        return config.PROPOSALS_PER_PAGE

    def get_context_data(self, **kwargs):
        # Add number of talks and tutorials to context data.
        context = super(ProposalListView, self).get_context_data(**kwargs)
        context["num_proposals"] = self.get_queryset().count()
        context["num_posters"] = (
            self.get_queryset().filter(kind__slug="poster").count()
        )
        context["num_talks"] = (
            self.get_queryset().filter(kind__name__endswith="Talk").count()
        )
        context["num_tutorials"] = (
            self.get_queryset().filter(kind__slug="tutorial").count()
        )
        if self.request.user.is_superuser:
            context["notification_form"] = ProposalNotificationForm()
        context["proposal_category"] = "All"
        context["proposal_kind"] = "Proposal"
        context["kind_list"] = ProposalKind.objects.order_by("name")

        # Add ARIA label for pagination.
        context["pagination_aria_label"] = "Proposal lists pages"

        return context


class ProposalKindListView(ProposalListView):
    def get(self, request, *args, **kwargs):
        try:
            self.proposal_kind = ProposalKind.objects.get(slug=kwargs["kind"])
        except ProposalKind.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        return (
            Proposal.objects.order_by("pk")
            .exclude(cancelled=True)
            .filter(kind=self.proposal_kind)
            .select_related("speaker", "review_result")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proposal_kind"] = self.proposal_kind.name
        return context


class ProposalReviewRequestedListView(ProposalListView):
    def get_queryset(self, **kwargs):
        user_votes = self.request.user.review_votes.filter(score=None)
        return (
            Proposal.objects.order_by("pk")
            .exclude(cancelled=True)
            .filter(review_votes__in=user_votes)
            .select_related("speaker", "review_result")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proposal_category"] = "Assigned"
        return context


class ProposalDetailView(DetailView, ReviewingView):
    allow_speakers = True
    context_object_name = "proposal"
    model = Proposal
    template_name = "reviews/proposal_detail.html"

    def get_context_data(self, **kwargs):
        """Add context as to whether this is a reviewer or speaker."""
        context = super(ProposalDetailView, self).get_context_data(**kwargs)
        if _is_reviewer_or_superuser(self.request.user):
            context["actor"] = "reviewer"
        for speaker in self.get_object().speakers():
            if self.request.user == speaker.user:
                context["actor"] = "speaker"
        try:
            vote = ProposalVote.objects.get(
                proposal=self.get_object(), voter=self.request.user
            )
            context["vote_form"] = ProposalVoteForm(instance=vote)
            if vote.score:
                context["existing_vote"] = True
        except ProposalVote.DoesNotExist:
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
        vote.score = int(self.request.POST["score"])
        vote.comment = self.request.POST["comment"]
        vote.save()

        return HttpResponseRedirect(
            reverse("review_proposal_detail", args=[proposal.id])
        )


class ProposalFeedbackPostView(ReviewingView):
    allow_speakers = True
    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        """AJAX update an individual ProposalVote object."""
        proposal = Proposal.objects.get(pk=kwargs["pk"])
        feedback = ProposalFeedback.objects.create(
            proposal=proposal,
            author=self.request.user,
            comment=self.request.POST["comment"],
        )
        # Send email to proposal speakers.
        speaker_email_addressses = []
        for speaker in proposal.speakers():
            # Only send messages to speakers with email addresses
            # who are not the author of this message.
            if (
                speaker.email
                and speaker.user
                and speaker.user != self.request.user
                and speaker.email not in speaker_email_addressses
            ):
                speaker_email_addressses.append(speaker.email)
        send_email(
            speaker_email_addressses,
            "proposal_new_message",
            context={
                "proposal": proposal,
                "message": feedback,
                "reviewer": False,
            },
        )
        # Send email to reviewers.
        reviewer_email_addresses = []
        for feedback in proposal.review_feedback.all():
            if (
                feedback.author.email
                and feedback.author != self.request.user
                and feedback.author.email not in reviewer_email_addresses
            ):
                reviewer_email_addresses.append(feedback.author.email)
        send_email(
            reviewer_email_addresses,
            "proposal_new_message",
            context={
                "proposal": proposal,
                "message": feedback,
                "reviewer": True,
            },
        )
        return HttpResponseRedirect(
            reverse("review_proposal_detail", args=[proposal.id])
        )
