import random

from django.core.cache import cache

from conf_site.accounts.tests import AccountsTestCase
from conf_site.reviews.models import ProposalVote, proposalvote_score_cache_key
from conf_site.reviews.signals import refresh_vote_counts
from conf_site.reviews.tests import ReviewingPostViewTestCase
from conf_site.reviews.tests.factories import ProposalVoteFactory


NUMERIC_SCORE_LIST = [score[0] for score in ProposalVote.SCORES]


class ProposalVotePostingTestCase(ReviewingPostViewTestCase, AccountsTestCase):
    reverse_view_name = "review_proposal_vote"

    def setUp(self):
        super().setUp()

        self.reverse_view_data = {
            "score": random.choice(NUMERIC_SCORE_LIST),
            "comment": self.faker.paragraph(
                nb_sentences=5, variable_nb_sentences=True
            ),
        }

    def _get_cached_vote_score(self):
        """Helper method to retrieve a cached vote score."""
        return cache.get(
            proposalvote_score_cache_key(self.proposal, self.user)
        )

    def test_cached_value(self):
        previous_vote = ProposalVoteFactory.build(
            proposal=self.proposal, voter=self.user
        )
        # Change the vote if it is the same as the score to be POSTed.
        while previous_vote.score == self.reverse_view_data["score"]:
            previous_vote.score = random.choice(NUMERIC_SCORE_LIST)
        previous_numeric_score = previous_vote.get_numeric_score_display()
        previous_vote.save()
        refresh_vote_counts(sender=None, instance=previous_vote, created=True)

        self.assertEqual(self._get_cached_vote_score(), previous_numeric_score)

        self._add_to_reviewers_group()
        response = self._get_response()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            self._get_cached_vote_score(), previous_numeric_score
        )
