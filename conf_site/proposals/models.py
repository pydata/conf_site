from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from multiselectfield import MultiSelectField
from symposion.proposals.models import ProposalBase


@python_2_unicode_compatible
class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    YES_NO_OTHER_YES = "Y"
    YES_NO_OTHER_NO = "N"
    # https://en.wikipedia.org/wiki/Bartleby,_the_Scrivener
    YES_NO_OTHER_BARTLEBY = "O"
    UNDER_REPRESENTED_ETHNICITY = "E"
    UNDER_REPRESENTED_AGE = "A"
    UNDER_REPRESENTED_GENDER = "G"
    UNDER_REPRESENTED_SEXUAL_ORIENTATION = "S"
    UNDER_REPRESENTED_DISABILITY = "D"
    UNDER_REPRESENTED_SOCIOECONOMIC = "C"
    UNDER_REPRESENTED_RELIGION = "R"
    UNDER_REPRESENTED_OPT_OUT = "O"
    UNDER_REPRESENTED_OTHER = "X"

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    YES_NO_OTHER_ANSWERS = (
        ("", "----"),
        (YES_NO_OTHER_YES, "Yes"),
        (YES_NO_OTHER_NO, "No"),
        (YES_NO_OTHER_BARTLEBY, "Prefer not to say"),
    )
    UNDER_REPRESENTED_DETAILED_ANSWERS = (
        (UNDER_REPRESENTED_GENDER, "Gender identity"),
        (UNDER_REPRESENTED_ETHNICITY, "Ethnicity, nationality, "
                                      "skin color, race"),
        (UNDER_REPRESENTED_SEXUAL_ORIENTATION, "Sexual orientation"),
        (UNDER_REPRESENTED_SOCIOECONOMIC, "Socioeconomic status"),
        (UNDER_REPRESENTED_RELIGION, "Religion"),
        (UNDER_REPRESENTED_AGE, "Age"),
        (UNDER_REPRESENTED_DISABILITY, "Ability"),
        (UNDER_REPRESENTED_OPT_OUT, "Do not wish to provide"),
        (UNDER_REPRESENTED_OTHER, "Other (please specify)"),
    )

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)

    slides_url = models.URLField(
        blank=True,
        default="",
        help_text=("Location of slides for this proposal "
                   "(e.g. SlideShare, Google Drive)."),
        max_length=2083,
        verbose_name="Slides")
    code_url = models.URLField(
        blank=True,
        default="",
        help_text="Location of this proposal's code repository (e.g. Github).",
        max_length=2083,
        verbose_name="Repository")

    first_time_at_pydata = models.CharField(
        "Is this your first time speaking at a PyData event?",
        choices=YES_NO_OTHER_ANSWERS,
        blank=True,
        default="",
        max_length=1)
    affiliation = models.CharField(blank=True, default="", max_length=200)
    under_represented_population = models.CharField(
        "Do you self-identify as an underrepresented minority in "
        "either the PyData/NumFOCUS community or in your "
        "professional field?",
        choices=YES_NO_OTHER_ANSWERS,
        default="",
        max_length=1)
    under_represented_details = MultiSelectField(
        "Along which dimension(s) you self-identify as underrepresented? "
        "Check all that apply:",
        blank=True,
        choices=UNDER_REPRESENTED_DETAILED_ANSWERS,
        max_choices=len(UNDER_REPRESENTED_DETAILED_ANSWERS))
    # Text for an prospoal submitter to input additional details about
    # their under represented dimensions.
    under_represented_other = models.CharField(
        "", blank=True, default="", max_length=200)

    phone_number = models.CharField(
        "Phone number - to be used for last-minute schedule changes",
        blank=True,
        default="",
        max_length=100)
    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your proposal, you agree to give permission "
                  "to the conference organizers to record, edit, and release "
                  "audio and/or video of your presentation. If you do not "
                  "agree to this, please uncheck this box."
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name="Created")
    date_last_modified = models.DateTimeField(
        auto_now=True,
        null=True,
        verbose_name="Last Modified")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Update associated presentation if it exists.
        if hasattr(self, "presentation") and self.presentation:
            self.presentation.title = self.title
            self.presentation.description = self.description
            self.presentation.abstract = self.abstract
            self.presentation.speaker = self.speaker
            for speaker in self.additional_speakers.all():
                    self.presentation.additional_speakers.add(speaker)
            self.presentation.section = self.section
            self.presentation.save()

        return super(Proposal, self).save(*args, **kwargs)
