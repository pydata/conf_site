from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from constance import config
from symposion.markdown_parser import parse
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
    YES_NO_OTHER_ANSWERS = (
        ("", "----"),
        (YES_NO_OTHER_YES, "Yes"),
        (YES_NO_OTHER_NO, "No"),
        (YES_NO_OTHER_BARTLEBY, "Prefer not to say"),
    )

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    audience_background = models.CharField(
        "Audience background needed to attend", blank=True, max_length=400
    )
    outline = models.TextField(
        _("Brief Bullet Point Outline"),
        blank=True,
    )
    outline_html = models.TextField(blank=True, editable=False)

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

    recording_online = models.BooleanField(
        _("Is there a recording of this talk/tutorial already online?"),
        default=False,
    )

    affiliation = models.CharField(max_length=200)

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
        # HTMLize markdown fields.
        self.outline_html = parse(self.outline)
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
