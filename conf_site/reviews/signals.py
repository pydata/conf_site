from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from conf_site.reviews.models import (
    ProposalFeedback,
    ProposalVote,
    proposalvote_score_cache_key,
)


@receiver(post_save, sender=ProposalFeedback)
def refresh_proposal_feedback_count(sender, instance, created, **kwargs):
    instance.proposal._refresh_feedback_count()


@receiver(post_save, sender=ProposalVote)
def refresh_vote_counts(sender, instance, created, **kwargs):
    # Update this ProposalVote's proposal's cached proposal votes.
    instance.proposal._refresh_vote_counts()
    # Update this voter's cached score for this proposal.
    cache_key = proposalvote_score_cache_key(instance.proposal, instance.voter)
    numeric_score = instance.get_numeric_score_display()
    cache.set(cache_key, numeric_score, settings.CACHE_TIMEOUT_LONG)
