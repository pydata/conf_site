# -*- coding: utf-8 -*-
from random import randint

from django.contrib.auth.models import Group
from django.urls import reverse

from constance.test import override_config

from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.reviews.tests.factories import ProposalFeedbackFactory


class ReviewingTestCase(object):
    """
    Base automated test case for reviewing application.

    This case has two parameters:
    reverse_view_name (string) - the name of the view to be reversed.
    reverse_view_args (list) - the arguments passed to the reversed view.

    """

    reverse_view_args = None

    def _add_to_reviewers_group(self):
        self.user.groups.add(self.reviewers_group)
        self.user.save()

    def _create_proposals(self):
        """Create proposals if needed to test a view."""
        try:
            # If we already have a proposal, this is a DetailView
            # and we shouldn't create more.
            return [self.proposal]
        except AttributeError:
            return ProposalFactory.create_batch(size=randint(2, 5))

    def setUp(self):
        super(ReviewingTestCase, self).setUp()

        self.reviewers_group = Group.objects.get_or_create(name="Reviewers")[0]
        # The majority of tests require user login.
        self.client.login(username=self.user.email, password=self.password)

    def test_no_anonymous_access(self):
        """Verify that anonymous users cannot access the view."""
        self.client.logout()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertEqual(response.status_code, 403)

    def test_superuser_access(self):
        """Verify that superusers can access the view."""
        self._become_superuser()
        self.assertFalse(self.reviewers_group in self.user.groups.all())
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertEqual(response.status_code, 200)

    def test_user_not_in_reviewers_group(self):
        """Verify that a non-reviewer cannot access the view."""
        self.assertFalse(self.reviewers_group in self.user.groups.all())
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertEqual(response.status_code, 403)

    def test_user_in_reviewers_group(self):
        """Verify that a reviewer can access the view."""
        self._add_to_reviewers_group()
        self.assertTrue(self.reviewers_group in self.user.groups.all())
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertEqual(response.status_code, 200)

    def test_blind_reviewing_types_as_reviewer(self):
        """Verify whether BLIND_REVIEWERS setting works properly."""
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
