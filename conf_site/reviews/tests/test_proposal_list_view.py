# -*- coding: utf-8 -*-
from django.urls import reverse

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
