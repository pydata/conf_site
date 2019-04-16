# -*- coding: utf-8 -*-
from random import randint
from django.urls import reverse

from symposion.proposals.models import ProposalKind
from symposion.schedule.tests.factories import SectionFactory

from conf_site.accounts.tests import AccountsTestCase
from conf_site.reviews.tests import ReviewingTestCase

from conf_site.proposals.tests.factories import ProposalFactory


class ProposalListViewAccessTestCase(ReviewingTestCase, AccountsTestCase):
    reverse_view_name = "review_proposal_list"

    def test_no_cancelled_proposals(self):
        """Verify that cancelled proposals do not appear in proposal list."""
        VALID_PROPOSAL_COUNT = 4
        INVALID_PROPOSAL_COUNT = 3

        # Create proposals.
        valid_proposals = ProposalFactory.create_batch(
            size=VALID_PROPOSAL_COUNT, cancelled=False
        )
        invalid_proposals = ProposalFactory.create_batch(
            size=INVALID_PROPOSAL_COUNT, cancelled=True
        )

        # User must be in the reviewers group in order to access
        # this view.
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        for valid_proposal in valid_proposals:
            self.assertContains(response, valid_proposal.title)
        for invalid_proposal in invalid_proposals:
            self.assertNotContains(response, invalid_proposal.title)

    def test_proposal_count(self):
        """Verify that proposal list contains count of proposals."""
        self._add_to_reviewers_group()
        # Setup the ProposalKinds for talks and tutorials.
        section = SectionFactory()
        talk_kind = ProposalKind.objects.create(
            section=section, name="Talk", slug="talk"
        )
        tutorial_kind = ProposalKind.objects.create(
            section=section, name="Tutorial", slug="tutorial"
        )
        # Create a random number of talks and tutorials.
        num_talks = randint(2, 10)
        num_tutorials = randint(2, 10)
        num_total_proposals = num_talks + num_tutorials
        ProposalFactory.create_batch(size=num_talks, kind=talk_kind)
        ProposalFactory.create_batch(size=num_tutorials, kind=tutorial_kind)

        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertContains(
            response,
            "<strong>{}</strong> proposals".format(num_total_proposals),
        )
        self.assertContains(
            response, "<strong>{}</strong> talks".format(num_talks)
        )
        self.assertContains(
            response, "<strong>{}</strong> tutorials".format(num_tutorials)
        )
