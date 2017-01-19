from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from multiselectfield import MultiSelectField
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
    UNDER_REPRESENTED_ETHNICITY = "E"
    UNDER_REPRESENTED_AGE = "A"
    UNDER_REPRESENTED_GENDER = "G"
    UNDER_REPRESENTED_SEXUAL_ORIENTATION = "S"
    UNDER_REPRESENTED_DISABILITY = "D"
    UNDER_REPRESENTED_OPT_OUT = "O"

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
    UNDER_REPRESENTED_DETAILED_ANSWERS = (
        (UNDER_REPRESENTED_ETHNICITY, "Ethnicity"),
        (UNDER_REPRESENTED_AGE, "Age"),
        (UNDER_REPRESENTED_GENDER, "Gender"),
        (UNDER_REPRESENTED_SEXUAL_ORIENTATION, "Sexual Orientation"),
        (UNDER_REPRESENTED_DISABILITY, "Disability"),
        (UNDER_REPRESENTED_OPT_OUT, "Opt-out"),
    )

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)

    under_represented_population = models.CharField(
        "Do you feel that you or your talk represent a "
        "population under-represented in the Python "
        "and/or Data community? In no way will this "
        "data be used as part of your proposal. This will only be "
        "used to gather diversity statistics in order to further "
        "NumFOCUS' mission.",
        choices=UNDER_REPRESENTED_ANSWERS,
        default="",
        max_length=1)
    under_represented_details = MultiSelectField(
        "Check all that apply:",
        blank=True,
        choices=UNDER_REPRESENTED_DETAILED_ANSWERS,
        max_choices=len(UNDER_REPRESENTED_DETAILED_ANSWERS))

    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your proposal, you agree to give permission "
                  "to the conference organizers to record, edit, and release "
                  "audio and/or video of your presentation. If you do not "
                  "agree to this, please uncheck this box."
    )

    def __str__(self):
        return self.title
