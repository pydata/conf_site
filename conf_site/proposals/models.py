from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from symposion.proposals.models import ProposalBase


@python_2_unicode_compatible
class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)

    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your proposal, you agree to give permission to "
                  "the conference organizers to record, edit, and release audio and/or "
                  "video of your presentation. If you do not agree to this, please uncheck "
                  "this box."
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class TalkProposal(Proposal):
    class Meta:
        verbose_name = "talk proposal"

    def __unicode__(self):
        return self.title

class TutorialProposal(Proposal):
    class Meta:
        verbose_name = "tutorial proposal"

    def __unicode__(self):
        return self.title
