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


class AcceptedSpeakerListViewTestCase(TestCase):
    """Verify that a presentation's primary & secondary speakers are shown."""

    def setUp(self):
        conference = Conference.objects.create(title="Conference")
        self.section = Section.objects.create(
            conference=conference, name="Section", slug="section"
        )
        schedule = Schedule.objects.create(section=self.section)
        self.day = Day.objects.create(
            schedule=schedule, date=timezone.now().date()
        )
        self.slot_kind = SlotKind.objects.create(
            schedule=schedule, label="slot kind"
        )
        self.proposal_kind = ProposalKind.objects.create(
            section=self.section, name="Kind", slug="kind"
        )

    def test_unaccepted_speakers(self):
        """Verify that speakers without presentations do not appear."""
        speaker = Speaker.objects.create(name="No Accepted Presentations")
        self.assertEqual(speaker.presentations.count(), 0)
        response = self.client.get(reverse("speaker_list"))
        self.assertNotContains(response, speaker.name)

    def test_no_duplicate_speakers(self):
        """Verify that a speaker is only shown once."""
        # Create a speaker with two accepted presentations.
        speaker = Speaker.objects.create(name="Two Accepted Presentations")
        Presentation.objects.create(
            slot=Slot.objects.create(
                day=self.day,
                kind=self.slot_kind,
                start=timezone.now(),
                end=timezone.now(),
            ),
            title="#1",
            description="Description",
            abstract="Abstract",
            speaker=speaker,
            proposal_base=ProposalBase.objects.create(
                title="#1",
                description="Description",
                abstract="Abstract",
                kind=self.proposal_kind,
                speaker=speaker,
            ),
            section=self.section,
        )
        Presentation.objects.create(
            slot=Slot.objects.create(
                day=self.day,
                kind=self.slot_kind,
                start=timezone.now(),
                end=timezone.now(),
            ),
            title="#2",
            description="Description",
            abstract="Abstract",
            speaker=speaker,
            proposal_base=ProposalBase.objects.create(
                title="#2",
                description="Description",
                abstract="Abstract",
                kind=self.proposal_kind,
                speaker=speaker,
            ),
            section=self.section,
        )
        self.assertEqual(speaker.presentations.count(), 2)
        response = self.client.get(reverse("speaker_list"))
        self.assertContains(response=response, text=speaker.name, count=1)

    def test_one_presentation_two_speakers(self):
        """Verify that secondary speakers appear in the speaker list."""
        speaker1 = Speaker.objects.create(name="Speaker Number One")
        speaker2 = Speaker.objects.create(name="Speaker Number Two")
        presentation = Presentation.objects.create(
            slot=Slot.objects.create(
                day=self.day,
                kind=self.slot_kind,
                start=timezone.now(),
                end=timezone.now(),
            ),
            title="#1",
            description="Description",
            abstract="Abstract",
            speaker=speaker1,
            proposal_base=ProposalBase.objects.create(
                title="#1",
                description="Description",
                abstract="Abstract",
                kind=self.proposal_kind,
                speaker=speaker1,
            ),
            section=self.section,
        )
        presentation.additional_speakers.add(speaker2)
        response = self.client.get(reverse("speaker_list"))
        self.assertContains(response=response, text=speaker1.name, count=1)
        self.assertContains(response=response, text=speaker2.name, count=1)
