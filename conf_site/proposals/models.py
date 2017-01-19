from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from symposion.proposals.models import ProposalBase


@python_2_unicode_compatible
class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    UNDER_REPRESENTED_YES = "Y"
    UNDER_REPRESENTED_NO = "N"
    # https://en.wikipedia.org/wiki/Bartleby,_the_Scrivener
    UNDER_REPRESENTED_BARTLEBY = "O"

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    UNDER_REPRESENTED_ANSWERS = (
        ("", "----"),
        (UNDER_REPRESENTED_YES, "Yes"),
        (UNDER_REPRESENTED_NO, "No"),
        (UNDER_REPRESENTED_BARTLEBY, "I would prefer not to answer"),
    )

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)

    under_represented_population = models.CharField(
        "Do you feel that you or your talk represent a "
        "population under-represented in the Python "
        "and/or Data community?",
        choices=UNDER_REPRESENTED_ANSWERS,
        default="",
        max_length=1)

    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your proposal, you agree to give permission "
                  "to the conference organizers to record, edit, and release "
                  "audio and/or video of your presentation. If you do not "
                  "agree to this, please uncheck this box."
    )

    def __str__(self):
        return self.title
