# -*- coding: utf-8 -*-
from django.urls import reverse

from constance.test import override_config

from conf_site.accounts.tests import AccountsTestCase
from conf_site.reviews.tests import ReviewingTestCase

from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.reviews.tests.factories import (
    ProposalFeedbackFactory,
    ProposalVoteFactory,
)


class ProposalDetailViewAccessTestCase(ReviewingTestCase, AccountsTestCase):
    reverse_view_name = "review_proposal_detail"

    def setUp(self):
        super(ProposalDetailViewAccessTestCase, self).setUp()
        self.proposal = ProposalFactory()
        self.reverse_view_args = [self.proposal.pk]

    def test_blind_reviewing_types_as_author(self):
        """Verify whether BLIND_AUTHORS setting works properly."""
        self._i_am_the_speaker_now()

        # Create a feedback comment, otherwise this test will pass
        # when it should fail.
        ProposalFeedbackFactory(
            proposal=self.proposal, author=self.reviewer.user
        )

        with override_config(BLIND_AUTHORS=True):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            self.assertNotContains(response, self.reviewer.name)
            self.assertNotContains(response, self.reviewer.user.username)
            self.assertNotContains(response, self.reviewer.email)

    def test_primary_speaker_cannot_view_votes_tab(self):
        """Verify that proposal speakers cannot view their proposal's votes."""
        self._i_am_the_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "proposal-reviews")

    def test_additional_speakers_cannot_view_votes_tab(self):
        """
        Verify that additional speakers cannot view their proposal's votes.
        """
        self._i_am_also_a_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "proposal-reviews")

    def test_reviewer_can_view_votes_tab(self):
        """Verify that a reviewer can view a proposal's votes."""
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertContains(response, "proposal-reviews")

    def test_primary_speaker_cannot_view_result_buttons(self):
        """Verify that proposal speakers cannot view result buttons section."""
        self._i_am_the_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "div-proposal-result-buttons")

    def test_additional_speakers_cannot_view_result_buttons(self):
        """Verify that additional speakers cannot view result buttons."""
        self._i_am_also_a_speaker_now()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "div-proposal-result-buttons")

    def test_reviewer_cannot_view_result_buttons(self):
        """
        Verify that proposal reviewers cannot view result buttons section.
        """
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(response, "div-proposal-result-buttons")

    def test_superuser_can_view_result_buttons(self):
        """Verify that superusers can view result buttons section."""
        self._become_superuser()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertContains(response, "div-proposal-result-buttons")

    def test_reviewer_cannot_view_other_reviewers_names(self):
        """Verify that a reviewer cannot view other reviewers' names."""
        other_vote = ProposalVoteFactory(proposal=self.proposal)
        other_feedback = ProposalFeedbackFactory.create(proposal=self.proposal)

        self._add_to_reviewers_group()
        with override_config(BLIND_REVIEWERS=True):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            self.assertNotContains(response, other_vote.voter.username)
            self.assertNotContains(response, other_vote.voter.email)

            self.assertNotContains(response, other_feedback.author.username)
            self.assertNotContains(response, other_feedback.author.email)

    def _test_button_text(self, good_text, bad_text):
        self._add_to_reviewers_group()
        response = self._get_response()
        self.assertContains(response, good_text)
        self.assertNotContains(response, bad_text)
        return response

    def test_submit_button_with_no_preexisting_vote(self):
        """Test that 'Submit Review' appears by default."""
        self._test_button_text("Submit Review", "Update Review")

    def test_submit_button_with_other_votes(self):
        """Test that other votes don't let 'Update Review' appear."""
        ProposalVoteFactory.create_batch(size=5, proposal=self.proposal)
        self._test_button_text("Submit Review", "Update Review")

    def test_update_button_with_preexisting_vote(self):
        """Test that 'Update Review' appears if reviewer has voted."""
        vote = ProposalVoteFactory.create(
            proposal=self.proposal, voter=self.user
        )
        response = self._test_button_text("Update Review", "Submit Review")
        # Vote comment should appear twice - once in the list of votes
        # and once in the form field.
        self.assertContains(response, vote.comment, 2)

    def test_non_review_answers_do_not_appear(self):
        """Test that reviewers cannot view speakers' non-review answers."""
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertNotContains(
            response, "Reviewers cannot view the following information"
        )
        self.assertNotContains(response, "Requests")
        self.assertNotContains(response, self.proposal.requests)
        self.assertNotContains(response, "Gender")
        self.assertNotContains(response, self.proposal.gender)
        self.assertNotContains(response, "Referral")
        self.assertNotContains(response, self.proposal.referral)
        self.assertNotContains(response, "Group Identity")
        self.assertNotContains(
            response, self.proposal.under_represented_group
        )
        self.assertNotContains(response, "Accessibility Needs")
        self.assertNotContains(response, self.proposal.accomodation_needs)
