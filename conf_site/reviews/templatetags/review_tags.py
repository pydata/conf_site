from django import template
from django.contrib.auth.models import Group

from conf_site.reviews.models import ProposalVote


register = template.Library()


@register.simple_tag
def user_score(proposal, user):
    """For the selected proposal, display the current user's review score."""
    try:
        score_display_string = ProposalVote.objects.get(
            proposal=proposal, voter=user
        ).get_score_display()
        # We only need the first two characters, without any spaces.
        return score_display_string[0:2].strip()
    except ProposalVote.DoesNotExist:
        return ""


@register.filter(name="is_reviewer")
def is_reviewer(user):
    """Determine whether selected user is in the Reviewers user group."""
    try:
        reviewers_group = Group.objects.get(name="Reviewers")
    except Group.DoesNotExist:
        return False
    return True if reviewers_group in user.groups.all() else False
