from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from symposion.conference.models import Conference, Section
from symposion.proposals.models import ProposalBase, ProposalKind
from symposion.schedule.models import (
    Presentation,
    Slot,
    SlotKind,
    Schedule,
    Day,
)
from symposion.speakers.models import Speaker


FIRST_PRESENTATION_TITLE = "Time Traveling with pandas"
SECOND_PRESENTATION_TITLE = "Last night, numpy saved my life"


class SpeakerProfilePresentationsTestCase(TestCase):
    """Tests relating to a speaker's presentations on their profile page."""

    def setUp(self):
        self.speaker = Speaker.objects.create(name="Paul Ryan")
        # Create base conference infrastructure.
        conference = Conference(title="Conference")
        conference.save()
        section = Section(
            conference=conference, name="Section", slug="section"
        )
        section.save()
        proposal_kind = ProposalKind(section=section, name="Kind", slug="kind")
        proposal_kind.save()
        first_proposal_base = ProposalBase.objects.create(
            title=FIRST_PRESENTATION_TITLE,
            description="Description",
            abstract="Abstract",
            kind=proposal_kind,
            speaker=self.speaker,
        )
        second_proposal_base = ProposalBase.objects.create(
            title=SECOND_PRESENTATION_TITLE,
            description="Description",
            abstract="Abstract",
            kind=proposal_kind,
            speaker=self.speaker,
        )

        # Note that saving ProposalResults will automatically
        # create or delete presentations. However, we want to test whether
        # presentations appear on speaker profile pages,
        # not whether ProposalResults create Presentations successfully.

        schedule = Schedule.objects.create(section=section)
        day = Day.objects.create(schedule=schedule, date=timezone.now().date())
        kind = SlotKind.objects.create(schedule=schedule, label="45-min talk")

        self.first_presentation = Presentation.objects.create(
            slot=Slot.objects.create(
                day=day, kind=kind, start=timezone.now(), end=timezone.now()
            ),
            title=FIRST_PRESENTATION_TITLE,
            description="Description",
            abstract="Abstract",
            speaker=self.speaker,
            proposal_base=first_proposal_base,
            section=section,
        )
        self.second_presentation = Presentation.objects.create(
            slot=Slot.objects.create(
                day=day, kind=kind, start=timezone.now(), end=timezone.now()
            ),
            title=SECOND_PRESENTATION_TITLE,
            description="Description",
            abstract="Abstract",
            speaker=self.speaker,
            proposal_base=second_proposal_base,
            section=section,
        )

    def test_display_presentation(self):
        """Verify that presentations display on speaker profiles."""
        response = self.client.get(
            reverse("speaker_profile", args=[self.speaker.pk])
        )
        self.assertContains(response, FIRST_PRESENTATION_TITLE)
        self.assertContains(response, SECOND_PRESENTATION_TITLE)

    def test_do_not_display_unscheduled_presentations(self):
        self.second_presentation.slot = None
        self.second_presentation.save()

        response = self.client.get(
            reverse("speaker_profile", args=[self.speaker.pk])
        )
        self.assertContains(response, FIRST_PRESENTATION_TITLE)
        self.assertNotContains(response, SECOND_PRESENTATION_TITLE)
