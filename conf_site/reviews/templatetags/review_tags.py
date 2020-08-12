from django import template
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache

from conf_site.reviews.models import ProposalVote, proposalvote_score_cache_key


register = template.Library()


@register.simple_tag
def user_score(proposal, user):
    """For the selected proposal, display the current user's review score."""
    # Try to retrieve score from cache.
    score_cache_key = proposalvote_score_cache_key(proposal, user)
    cached_score = cache.get(score_cache_key)
    if cached_score:
        return cached_score
    try:
        uncached_score = ProposalVote.objects.get(
            proposal=proposal, voter=user
        ).get_numeric_score_display()
    except ProposalVote.DoesNotExist:
        uncached_score = " "
    cache.set(score_cache_key, uncached_score, settings.CACHE_TIMEOUT_LONG)
    return uncached_score


@register.simple_tag
def user_vote_count(user, score_type):
    """Retrieve the number of reviews by a user."""
    return ProposalVote.objects.filter(voter=user, score=score_type).count()


@register.filter(name="is_reviewer")
def is_reviewer(user):
    """Determine whether selected user is in the Reviewers user group."""
    try:
        reviewers_group = Group.objects.get(name="Reviewers")
    except Group.DoesNotExist:
        return False
    return True if reviewers_group in user.groups.all() else False
