from django.conf import settings
from django.core.cache import cache
from django.db import models

from constance import config
from multiselectfield import MultiSelectField
from symposion.proposals.models import ProposalBase, ProposalSection
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

from conf_site.reviews.models import ProposalVote
from symposion.markdown_parser import parse


class ProposalKeyword(TagBase):
    official = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"


class ProposalTrack(TagBase):
    class Meta:
        verbose_name = "Track"
        verbose_name_plural = "Tracks"


class EditorTaggedProposal(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ProposalKeyword,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class TaggedProposal(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ProposalKeyword,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class UserTaggedProposal(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ProposalKeyword,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class TrackTaggedProposal(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ProposalTrack,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class Proposal(ProposalBase):

    YES_NO_OTHER_YES = "Y"
    YES_NO_OTHER_NO = "N"
    # https://en.wikipedia.org/wiki/Bartleby,_the_Scrivener
    YES_NO_OTHER_BARTLEBY = "O"

    UNDER_REPRESENTED_ETHNICITY = "R"
    UNDER_REPRESENTED_AGE = "A"
    UNDER_REPRESENTED_GENDER = "G"
    UNDER_REPRESENTED_SEXUAL_ORIENTATION = "S"
    UNDER_REPRESENTED_DISABILITY = "D"
    UNDER_REPRESENTED_SOCIOECON = "C"
    UNDER_REPRESENTED_EDUCATION = "E"
    UNDER_REPRESENTED_OPT_OUT = "O"
    UNDER_REPRESENTED_OTHER = "X"

    KNOWLEDGE_LEVELS = [
        (YES_NO_OTHER_NO, "No previous knowledge expected"),
        (YES_NO_OTHER_YES, "Previous knowledge expected"),
    ]
    YES_NO_BOOL_ANSWERS = (
        (True, "Yes"),
        (False, "No"),
    )
    YES_NO_OTHER_ANSWERS = (
        ("", "----"),
        (YES_NO_OTHER_YES, "Yes"),
        (YES_NO_OTHER_NO, "No"),
        (YES_NO_OTHER_BARTLEBY, "Prefer not to say"),
    )
    YES_NO_SPONSOR_ANSWERS = (
        ("", "----"),
        (YES_NO_OTHER_YES, "Yes, I can make an introduction"),
        (YES_NO_OTHER_NO, "No"),
    )
    UNDER_REPRESENTED_DETAILED_ANSWERS = (
        (UNDER_REPRESENTED_GENDER, "Gender identity"),
        (UNDER_REPRESENTED_SEXUAL_ORIENTATION, "Sexual orientation"),
        (UNDER_REPRESENTED_ETHNICITY, "Race or ethnicity"),
        (UNDER_REPRESENTED_AGE, "Age"),
        (UNDER_REPRESENTED_EDUCATION, "Educational background"),
        (UNDER_REPRESENTED_SOCIOECON, "Socioeconomic status or background"),
        (UNDER_REPRESENTED_DISABILITY, "Disability status"),
        (UNDER_REPRESENTED_OPT_OUT, "I decline to answer"),
        (UNDER_REPRESENTED_OTHER, "Other (please specify)"),
    )

    AFFILIATION_COMPANY = "C"
    AFFILIATION_SCHOOL = "S"
    AFFILIATION_INDEPENDENT = "I"
    AFFILIATIONS = (
        (AFFILIATION_COMPANY, "Company"),
        (AFFILIATION_SCHOOL, "School"),
        (AFFILIATION_INDEPENDENT, "Independent"),
    )

    prior_knowledge = models.CharField(
        choices=KNOWLEDGE_LEVELS,
        max_length=1,
        verbose_name="Prior Knowledge Expected",
    )
    prior_knowledge_details = models.CharField(
        blank=True,
        max_length=200,
        verbose_name=(
            "To attend the presentation, "
            "it would be recommended that "
            "the participant have some knowledge in:"
        ),
    )

    outline = models.TextField(
        "Brief Bullet Point Outline",
        blank=True,
        help_text=(
            "Brief outline. Will be made public "
            "if your proposal is accepted. Edit using "
            "<a href='https://daringfireball.net/projects/markdown/basics' "
            "target='_blank'>Markdown</a>."
        ),
    )
    outline_html = models.TextField(blank=True, editable=False)

    recording_online = models.BooleanField(
        "Is there a recording of this talk/tutorial already online?",
        default=False,
    )
    recording_url = models.URLField(
        blank=True, max_length=2083, verbose_name="If yes, what is the link?"
    )

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

    country = models.CharField(
        max_length=200, verbose_name="What is your country of residence?"
    )

    first_time_at_pydata = models.CharField(
        "Are you a first-time speaker?",
        choices=YES_NO_OTHER_ANSWERS,
        blank=True,
        default="",
        max_length=1)
    travel_at_own_expense = models.BooleanField(
        choices=YES_NO_BOOL_ANSWERS,
        default=True,
        verbose_name=(
            "Are you able to travel to Eindhoven at your own expense?"
        ),
    )
    affiliation = models.CharField(
        max_length=200,
        verbose_name="Affilation (Company, School, Independent)",
    )

    mentorship = models.BooleanField(
        choices=YES_NO_BOOL_ANSWERS,
        default=False,
        verbose_name=(
            "Would you like to be considered "
            "for our speaker mentorship program?"
        ),
    )
    mentoring = models.BooleanField(
        choices=YES_NO_BOOL_ANSWERS,
        default=False,
        verbose_name="Would you be interested in mentoring other speakers?",
    )

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

    accessibility_needs = models.CharField(
        "Do you have specific accessibility needs at the conference?",
        blank=True,
        max_length=1083,
    )
    under_represented_group = models.CharField(
        (
            "Do you identify as a member of an under-represented group "
            "in computing?"
        ),
        choices=YES_NO_OTHER_ANSWERS,
        default="",
        max_length=1,
    )
    under_represented_details = MultiSelectField(
        "I identify as a member of the following underrepresented group(s):",
        blank=True,
        choices=UNDER_REPRESENTED_DETAILED_ANSWERS,
        max_choices=len(UNDER_REPRESENTED_DETAILED_ANSWERS),
    )
    # Text for an prospoal submitter to input additional details about
    # their under represented dimensions.
    under_represented_other = models.CharField(
        "", blank=True, default="", max_length=200
    )
    sponsoring_interest = models.CharField(
        "Would your company be interested in sponsoring the event?",
        choices=YES_NO_SPONSOR_ANSWERS,
        default="",
        max_length=1,
    )
    tracks = TaggableManager(
        blank=True,
        related_name="track_tagged_proposals",
        through=TrackTaggedProposal,
        verbose_name="Tracks",
    )

    editor_keywords = TaggableManager(
        "Editor Keywords",
        blank=True,
        help_text="",
        related_name="editor_tagged_proposals",
        through=EditorTaggedProposal)
    official_keywords = TaggableManager(
        "Keywords",
        blank=True,
        help_text="",
        related_name="official_tagged_proposals",
        through=TaggedProposal)
    user_keywords = TaggableManager(
        "Additional Keywords",
        blank=True,
        help_text="Please add keywords as a comma-separated list.",
        related_name="user_tagged_proposals",
        through=UserTaggedProposal)

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

        # HTML-ize outline field.
        self.outline_html = parse(self.outline)

        return super(Proposal, self).save(*args, **kwargs)

    def _feedback_count_cache_key(self):
        return "proposal_{}_feedback_count".format(self.pk)

    def _get_cached_vote_count(self, cache_key, vote_score):
        """Helper method to retrieve cached vote counts."""
        cached_vote_count = cache.get(cache_key, False)
        if cached_vote_count is not False:
            return cached_vote_count
        vote_count = ProposalVote.objects.filter(
            proposal=self, score=vote_score
        ).count()
        # We can use a longer timeout because we update invididual
        # vote counts when ProposalVotes are created or modified.
        cache.set(cache_key, vote_count, settings.CACHE_TIMEOUT_LONG)
        return vote_count

    def _refresh_feedback_count(self):
        """Helper method to manually refresh a proposal's feedback count."""
        cache_key = self._feedback_count_cache_key()
        feedback_count = self.review_feedback.count()
        cache.set(cache_key, feedback_count, settings.CACHE_TIMEOUT_LONG)
        return feedback_count

    def _refresh_vote_counts(self):
        """Helper method to manually refresh a proposal's vote counts."""
        vote_count_dict = {
            "proposal_{}_plus_one".format(self.pk): ProposalVote.PLUS_ONE,
            "proposal_{}_plus_zero".format(self.pk): ProposalVote.PLUS_ZERO,
            "proposal_{}_minus_zero".format(self.pk): ProposalVote.MINUS_ZERO,
            "proposal_{}_minus_one".format(self.pk): ProposalVote.MINUS_ONE,
        }
        for cache_key, vote_score in vote_count_dict.items():
            vote_count = ProposalVote.objects.filter(
                proposal=self, score=vote_score
            ).count()
            cache.set(cache_key, vote_count, settings.CACHE_TIMEOUT_LONG)

    def can_edit(self):
        if config.PROPOSAL_EDITING_WHEN_CFP_IS_CLOSED:
            return True

        # Determine whether this proposal's ProposalSection is open.
        proposal_section = ProposalSection.objects.get(section=self.section)
        return proposal_section.available()

    def feedback_count(self):
        """Helper method to retrieve feedback count."""
        cache_key = self._feedback_count_cache_key()
        feedback_count = cache.get(cache_key, False)
        if feedback_count is not False:
            return feedback_count
        return self._refresh_feedback_count()

    @property
    def plus_one(self):
        """Enumerate number of +1 reviews."""
        return self._get_cached_vote_count(
            "proposal_{}_plus_one".format(self.pk), ProposalVote.PLUS_ONE
        )

    @property
    def plus_zero(self):
        """Enumerate number of +0 reviews."""
        return self._get_cached_vote_count(
            "proposal_{}_plus_zero".format(self.pk), ProposalVote.PLUS_ZERO
        )

    @property
    def minus_zero(self):
        """Enumerate number of -0 reviews."""
        return self._get_cached_vote_count(
            "proposal_{}_minus_zero".format(self.pk), ProposalVote.MINUS_ZERO,
        )

    @property
    def minus_one(self):
        """Enumerate number of -1 reviews."""
        return self._get_cached_vote_count(
            "proposal_{}_minus_one".format(self.pk), ProposalVote.MINUS_ONE
        )

    @property
    def total_votes(self):
        return (
            self.plus_one + self.plus_zero + self.minus_zero + self.minus_one
        )
