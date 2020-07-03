from django.conf import settings
from django.core.cache import cache
from django.db import models

from constance import config
from symposion.proposals.models import ProposalBase, ProposalSection
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

from conf_site.reviews.models import ProposalVote


class ProposalKeyword(TagBase):
    official = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"


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


class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    YES_NO_OTHER_YES = "Y"
    YES_NO_OTHER_NO = "N"
    # https://en.wikipedia.org/wiki/Bartleby,_the_Scrivener
    YES_NO_OTHER_BARTLEBY = "O"

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
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

    PROPOSAL_TRACK_NA = 0
    PROPOSAL_TRACK_ALGORITHMS = 1
    PROPOSAL_TRACK_METHODS = 2
    PROPOSAL_TRACK_PRODUCTION = 3
    PROPOSAL_TRACK_VISUAL = 4
    PROPOSAL_TRACK_JULIA = 5
    PROPOSAL_TRACK_LESSONS = 6
    PROPOSAL_TRACK_OPEN_SCIENCE = 7
    PROPOSAL_TRACKS = (
        (PROPOSAL_TRACK_NA, "Not Applicable"),
        (PROPOSAL_TRACK_ALGORITHMS, "Algorithmic Accountability"),
        (PROPOSAL_TRACK_METHODS, "Causal and Statistical Methods"),
        (PROPOSAL_TRACK_PRODUCTION, "Data Science in Production"),
        (PROPOSAL_TRACK_VISUAL, "Data Visualization & Interpretability"),
        (PROPOSAL_TRACK_JULIA, "Julia for Python Users & Julia Users"),
        (PROPOSAL_TRACK_LESSONS, "Lessons from Industry"),
        (PROPOSAL_TRACK_OPEN_SCIENCE, "Open Science"),
    )

    FIRST_TIME_ANY = "1"
    FIRST_TIME_THREE_PLUS = "2"
    FIRST_TIME_THREE_MINUS = "3"
    FIRST_TIME_ANSWERS = (
        ("", "----"),
        (YES_NO_OTHER_NO, "No"),
        (FIRST_TIME_ANY, "Yes - First-time technical speaker (any)"),
        (FIRST_TIME_THREE_PLUS, "Yes - First-time speaker (PyData) with 3+ conference talks"),      # noqa: E501
        (FIRST_TIME_THREE_MINUS, "Yes - First-time speaker (PyData) with < 3 conference talks"),    # noqa: E501
    )

    AFFILIATION_COMPANY = "C"
    AFFILIATION_SCHOOL = "S"
    AFFILIATION_INDEPENDENT = "I"
    AFFILIATIONS = (
        (AFFILIATION_COMPANY, "Company"),
        (AFFILIATION_SCHOOL, "School"),
        (AFFILIATION_INDEPENDENT, "Independent"),
    )

    MENTORING_TECH = "T"
    MENTORING_COMM = "C"
    MENTORING_BOTH = "B"
    MENTORING_CHOICES = (
        (YES_NO_OTHER_YES, "Yes"),
        (YES_NO_OTHER_NO, "No"),
        (MENTORING_TECH, "Yes, providing technical mentorship"),
        (MENTORING_COMM, "Yes, providing communication mentorship"),
        (MENTORING_BOTH, "Yes, both technical and communication mentoring"),
    )

    COMPANY_SPONSOR_CHOICES = (
        (True, "Yes, I can make an introduction"),
        (False, "No"),
    )

    AV_EQUIPMENT_NO = 0
    AV_EQUIPMENT_AUDIO = 1
    AV_EQUIPMENT_VIDEO = 2
    AV_EQUIPMENT_BOTH = 3
    AV_EQUIPMENT_CHOICES = (
        (AV_EQUIPMENT_NO, "No"),
        (AV_EQUIPMENT_AUDIO, "Yes, audio"),
        (AV_EQUIPMENT_VIDEO, "Yes, video"),
        (AV_EQUIPMENT_BOTH, "Yes, both"),
    )

    audience_level = models.IntegerField(
        choices=AUDIENCE_LEVELS, default=AUDIENCE_LEVEL_INTERMEDIATE,
    )

    already_recording = models.BooleanField(
        choices=YES_NO_BOOL_ANSWERS,
        default=False,
        verbose_name=(
            "Is there a recording of this talk/tutorial already online?"
        ),
    )
    recording_url = models.URLField(
        blank=True,
        default="",
        max_length=2083,
        verbose_name="If yes, what is the link?",
    )

    specialized_track = models.IntegerField(
        choices=PROPOSAL_TRACKS,
        default=PROPOSAL_TRACK_NA,
        verbose_name="Please choose a specialized track, if any",
    )

    other_language = models.CharField(
        blank=True,
        default="",
        max_length=100,
        verbose_name=(
            "Would this content be presented in a language other than English?"
            " If so, please indicate here."
        ),
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

    first_time_at_pydata = models.CharField(
        "Is this your first time speaking at a PyData event?",
        choices=FIRST_TIME_ANSWERS,
        blank=True,
        default="",
        max_length=1)
    affiliation = models.CharField(choices=AFFILIATIONS, max_length=1)

    commitment = models.BooleanField(
        choices=YES_NO_BOOL_ANSWERS,
        verbose_name=(
            "We are asking all speakers to commit to presenting "
            "at PyData Global 2020 if their proposals are accepted. "
            "This commitment will greatly simplify the Program Committee’s "
            "deliberations and will enable us to communicate acceptances and "
            "bring together the conference program much more quickly. "
            "If accepted, can you commit to presenting at PyData Global 2020?"
        ),
    )
    mentorship = models.BooleanField(
        choices=YES_NO_BOOL_ANSWERS,
        default=False,
        verbose_name=(
            "Would you like to be considered "
            "for our speaker mentorship program?"
        ),
    )
    mentoring = models.CharField(
        choices=MENTORING_CHOICES,
        max_length=1,
        verbose_name="Would you be interested in mentoring other speakers?",
    )

    company_sponsor_intro = models.BooleanField(
        choices=COMPANY_SPONSOR_CHOICES,
        verbose_name=(
            "Would your company be interested in sponsoring the event?"
        )
    )

    av_equipment_needed = models.IntegerField(
        choices=AV_EQUIPMENT_CHOICES,
        default=AV_EQUIPMENT_NO,
        verbose_name="Do you need audio and/or video recording equipment?",
    )
    av_needs = models.TextField(
        blank=True, verbose_name="If yes, describe your A/V needs."
    )

    stipend = models.BooleanField(
        default=False,
        help_text=(
            "We have a number of modest speaker stipends available "
            "based on need; the quantity available will depend on successful "
            "sponsorship of this effort. If a stipend would make a difference "
            "in your ability to prepare and record your material, "
            "and participate in live Q&A, please check this box for "
            "consideration for this funding. "
            "Proposal selection is need-blind; asking to be considered for "
            "need-based stipends will have no bearing on the consideration "
            "or likelihood of acceptance of your proposal."
        ),
        verbose_name="I would like to be considered for a stipend",
    )
    stipend_amount = models.CharField(
        blank=True,
        default="",
        max_length=100,
        verbose_name=(
            "If yes, please provide an estimated amount for the stipend."
        ),
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

    editor_keywords = TaggableManager(
        "Editor Keywords",
        blank=True,
        help_text="",
        related_name="editor_tagged_proposals",
        through=EditorTaggedProposal)
    official_keywords = TaggableManager(
        "Official Keywords",
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

    experience = models.BooleanField(
        default=False,
        choices=YES_NO_BOOL_ANSWERS,
        verbose_name="Have you presented at a conference before?",
    )

    merge_ability = models.BooleanField(
        default=False,
        choices=YES_NO_BOOL_ANSWERS,
        verbose_name=(
            "Will you be able to merge PRs in real-time during the sprint?"
        ),
    )
    attendance = models.CharField(
        blank=True,
        default="",
        max_length=100,
        verbose_name=(
            "Who else (if anyone) from the project is likely to attend?"
        ),
    )
    num_attendees = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=(
            "Approximately how many attendees would be ideal for you "
            "to accommodate in the sprint?"
        ),
    )
    issue_curation = models.BooleanField(
        default=False,
        choices=YES_NO_BOOL_ANSWERS,
        verbose_name=(
            "Will you be able to curate issues for first-time attendees "
            "to work on ahead of the sprint?"
        ),
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
        return proposal_section.is_available()

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
