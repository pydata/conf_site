# -*- coding: utf-8 -*-
from random import randint

from django.contrib.auth.models import Group
from django.urls import reverse

from constance.test import override_config
from faker import Faker

from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.reviews.tests.factories import ProposalFeedbackFactory
from conf_site.speakers.tests.factories import SpeakerFactory
from symposion.proposals.models import AdditionalSpeaker


class ReviewingMixin(object):
    def _add_to_reviewers_group(self):
        self.user.groups.add(self.reviewers_group)
        self.user.save()

    def _get_response(self):
        return self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )

    def setUp(self):
        super().setUp()

        self.reviewers_group = Group.objects.get_or_create(name="Reviewers")[0]
        # The majority of tests require user login.
        self.client.login(username=self.user.email, password=self.password)


class ReviewingNoAnonymousMixin(ReviewingMixin):
    def test_no_anonymous_access(self):
        """Verify that anonymous users cannot access the view."""
        self.client.logout()
        response = self._get_response()
        self.assertEqual(response.status_code, 403)


class ReviewingSuperuserMixin(ReviewingNoAnonymousMixin):
    def test_superuser_access(self):
        """Verify that superusers can access the view."""
        self._become_superuser()
        self.assertFalse(self.reviewers_group in self.user.groups.all())
        response = self._get_response()
        self.assertEqual(response.status_code, 200)


class ReviewingTestCase(ReviewingSuperuserMixin):
    """
    Base automated test case for reviewing application.

    This case has three required parameters:
    http_method_name (string) - either "get" or "post".
    reverse_view_name (string) - the name of the view to be reversed.
    reverse_view_args (list) - the arguments passed to the reversed view.

    """

    http_method_name = "get"
    reverse_view_args = None

    def _create_proposals(self):
        """Create proposals if needed to test a view."""
        try:
            # If we already have a proposal, this is a DetailView
            # and we shouldn't create more.
            return [self.proposal]
        except AttributeError:
            return ProposalFactory.create_batch(size=randint(2, 5))

    def _i_am_the_speaker_now(self):
        """Make this testcase's user the primary speaker of the proposal."""
        # Create a reviewer (as a speaker profile).
        self.reviewer = SpeakerFactory()
        # Attach current user as the primary speaker on this proposal.
        self.proposal.speaker.user = self.user
        self.proposal.speaker.save()

    def _i_am_also_a_speaker_now(self):
        """Make this testcase's user an additional speaker on the proposal."""
        self.reviewer = SpeakerFactory()
        self.reviewer.user = self.user
        self.reviewer.save()
        AdditionalSpeaker.objects.create(
            proposalbase=self.proposal.proposalbase_ptr,
            speaker=self.reviewer,
            status=AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED,
        )

    def test_user_not_in_reviewers_group(self):
        """Verify that a non-reviewer cannot access the view."""
        self.assertFalse(self.reviewers_group in self.user.groups.all())
        response = self._get_response()
        self.assertEqual(response.status_code, 403)

    def test_user_in_reviewers_group(self):
        """Verify that a reviewer can access the view."""
        self._add_to_reviewers_group()
        self.assertTrue(self.reviewers_group in self.user.groups.all())
        response = self._get_response()
        self.assertEqual(response.status_code, 200)

    def test_blind_reviewing_types_as_reviewer(self):
        """Verify whether BLIND_REVIEWERS setting works properly."""
        # This is not applicable for POSTing views.
        if self.http_method_name == "post":
            return
        self._add_to_reviewers_group()
        proposals = self._create_proposals()
        for proposal in proposals:
            # Create feedback from a random user.
            ProposalFeedbackFactory(proposal=proposal)
            # Create feedback from the proposal's speaker.
            ProposalFeedbackFactory(
                proposal=proposal, author=proposal.speaker.user
            )

        with override_config(BLIND_REVIEWERS=True):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            for proposal in proposals:
                self.assertNotContains(response, proposal.speaker.name)
                self.assertNotContains(
                    response, proposal.speaker.user.username
                )
                self.assertNotContains(response, proposal.speaker.email)

        with override_config(BLIND_REVIEWERS=False):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            for proposal in proposals:
                self.assertContains(response, proposal.speaker.name)

    def test_blind_reviewers_as_superuser(self):
        """Verify that superusers ignore the BLIND_REVIEWERS setting."""
        # This is not applicable for POSTing views.
        if self.http_method_name == "post":
            return
        self._become_superuser()
        proposals = self._create_proposals()
        for proposal in proposals:
            ProposalFeedbackFactory(proposal=proposal)

        with override_config(BLIND_REVIEWERS=True):
            response = self.client.get(
                reverse(self.reverse_view_name, args=self.reverse_view_args)
            )
            self.assertContains(response, "Your superuser status")
            for proposal in proposals:
                self.assertContains(response, proposal.speaker.name)


class ReviewingPostViewTestCase(ReviewingTestCase):
    http_method_name = "post"

    def setUp(self):
        super().setUp()

        self.faker = Faker()
        self.proposal = ProposalFactory()
        self.reverse_view_args = [self.proposal.pk]

    def _get_response(self):
        return self.client.post(
            reverse(self.reverse_view_name, args=self.reverse_view_args),
            data=self.reverse_view_data,
            follow=True,
        )
