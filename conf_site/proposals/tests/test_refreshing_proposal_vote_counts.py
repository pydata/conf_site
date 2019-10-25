from random import randint

from django.core.cache import cache

from conf_site.proposals.tests import ProposalTestCase
from conf_site.reviews.models import ProposalVote
from conf_site.reviews.tests.factories import ProposalVoteFactory


class ProposalVoteCountRefreshTestCase(ProposalTestCase):
    def setUp(self):
        super(ProposalVoteCountRefreshTestCase, self).setUp()
        self.vote_cache_keys = [
            "proposal_{}_plus_one".format(self.proposal.pk),
            "proposal_{}_plus_zero".format(self.proposal.pk),
            "proposal_{}_minus_zero".format(self.proposal.pk),
            "proposal_{}_minus_one".format(self.proposal.pk),
        ]

    def test_no_votes(self):
        """Verify that refreshing counts returns zero if there are no votes."""
        # Make sure that this proposal has no votes.
        self.assertEqual(self.proposal.review_votes.count(), 0)
        self.proposal._refresh_vote_counts()
        for cache_key in self.vote_cache_keys:
            self.assertEqual(cache.get(cache_key), 0)

    def test_setting_votes(self):
        # Create a random assortment of votes on our proposal.
        plus_one_votes = ProposalVoteFactory.create_batch(
            size=randint(0, 3),
            proposal=self.proposal,
            score=ProposalVote.PLUS_ONE,
        )
        plus_zero_votes = ProposalVoteFactory.create_batch(
            size=randint(0, 3),
            proposal=self.proposal,
            score=ProposalVote.PLUS_ZERO,
        )
        minus_zero_votes = ProposalVoteFactory.create_batch(
            size=randint(0, 3),
            proposal=self.proposal,
            score=ProposalVote.MINUS_ZERO,
        )
        minus_one_votes = ProposalVoteFactory.create_batch(
            size=randint(0, 3),
            proposal=self.proposal,
            score=ProposalVote.MINUS_ONE,
        )

        self.proposal._refresh_vote_counts()

        # Tally up vote counts and verify that the cached value is correct.
        vote_counts = [
            len(plus_one_votes),
            len(plus_zero_votes),
            len(minus_zero_votes),
            len(minus_one_votes),
        ]
        for index, cache_key in enumerate(self.vote_cache_keys):
            self.assertEqual(cache.get(cache_key), vote_counts[index])
