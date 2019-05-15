# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from symposion.utils.mail import send_email

from conf_site.proposals.models import Proposal
from conf_site.reviews.forms import ProposalFeedbackForm, ProposalVoteForm
from conf_site.reviews.models import ProposalFeedback, ProposalVote


class ReviewingView(UserPassesTestMixin, View):
    allow_speakers = False
    raise_exception = True

    def test_func(self):
        """Check if user can access reviewing section."""
        # Raise an exception if the Reviewers group does not
        # exist, because this is a critical problem.
        try:
            reviewers_group = Group.objects.get(name="Reviewers")
        except Group.DoesNotExist:
            raise Exception("Reviewers user group does not exist.")

        # Superusers always get access.
        if self.request.user.is_superuser:
            return True
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
        # Users in the Reviewers group also get access.
        return reviewers_group in self.request.user.groups.all()


class ProposalListView(ListView, ReviewingView):
    template_name = "reviews/proposal_list.html"

    def get_queryset(self, **kwargs):
        """Show all proposals, except those that have been cancelled."""
        return Proposal.objects.order_by("pk").exclude(cancelled=True)

    def get_context_data(self, **kwargs):
        # Add number of talks and tutorials to context data.
        context = super(ProposalListView, self).get_context_data(**kwargs)
        context["num_talks"] = (
            self.get_queryset().filter(kind__slug="talk").count()
        )
        context["num_tutorials"] = (
            self.get_queryset().filter(kind__slug="tutorial").count()
        )

        context["proposal_category"] = "All"
        return context


class ProposalDetailView(DetailView, ReviewingView):
    allow_speakers = True
    context_object_name = "proposal"
    model = Proposal
    template_name = "reviews/proposal_detail.html"

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
            if feedback.author.email and feedback.author != self.request.user:
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
