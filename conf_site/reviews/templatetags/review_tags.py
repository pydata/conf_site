from django import template

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
