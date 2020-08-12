from random import randint

from django.urls import reverse

from conf_site.proposals.tests.factories import (
    ProposalFactory,
    ProposalKindFactory,
)
from conf_site.reviews.tests.test_proposal_list_view import (
    ProposalListViewTestCase,
)


class ProposalKindListViewTestCase(ProposalListViewTestCase):
    reverse_view_name = "review_proposal_kind_list"

    def setUp(self):
        super().setUp()

        self.proposal_kind = ProposalKindFactory.create()
        self.reverse_view_args = [self.proposal_kind.slug]

    # Disable reviewing methods that are not valid for this view
    # because it contains a subset of all proposals.
    def test_blind_reviewing_types_as_reviewer(self):
        pass

    def test_blind_reviewers_as_superuser(self):
        pass

    def test_review_requested_proposal_status(self):
        pass

    def test_no_cancelled_proposals(self):
        """Verify that cancelled proposals do not appear in proposal list."""
        VALID_PROPOSAL_COUNT = 4
        INVALID_PROPOSAL_COUNT = 3

        # Create proposals - with this proposal kind.
        valid_proposals = ProposalFactory.create_batch(
            size=VALID_PROPOSAL_COUNT, kind=self.proposal_kind, cancelled=False
        )
        invalid_proposals = ProposalFactory.create_batch(
            size=INVALID_PROPOSAL_COUNT,
            kind=self.proposal_kind,
            cancelled=True,
        )

        self._validate_proposals(valid_proposals, True)
        self._validate_proposals(invalid_proposals, False)

    def test_proposal_count(self):
        self._add_to_reviewers_group()

        num_proposals = randint(2, 10)
        ProposalFactory.create_batch(
            size=num_proposals, kind=self.proposal_kind
        )
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertContains(
            response,
            "<strong>{}</strong> proposals".format(num_proposals),
        )

    def test_invalid_kind(self):
        """Verify that a random kind returns a 404."""
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=[self.faker.word()])
        )
        self.assertEqual(response.status_code, 404)

    def test_correct_information(self):
        """Verify that shown proposals are correct."""
        self._add_to_reviewers_group()
        shown_proposals = ProposalFactory.create_batch(
            size=randint(5, 10), kind=self.proposal_kind
        )
        unshown_proposals = ProposalFactory.create_batch(size=randint(5, 10))

        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        for proposal in shown_proposals:
            self.assertContains(response, proposal.title)
        for proposal in unshown_proposals:
            self.assertNotContains(response, proposal.title)
