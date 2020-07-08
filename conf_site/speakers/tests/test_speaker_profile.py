from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from faker import Faker
from symposion.conference.models import Conference, Section
from symposion.proposals.models import ProposalBase
from symposion.schedule.models import (
    Presentation,
    Slot,
    SlotKind,
    Schedule,
    Day,
)
from symposion.schedule.tests.factories import ProposalKindFactory
from symposion.speakers.models import Speaker


FIRST_PRESENTATION_TITLE = "Time Traveling with pandas"
SECOND_PRESENTATION_TITLE = "Last night, numpy saved my life"


class SpeakerProfileTestCase(TestCase):
    """Tests relating to a speaker's profile page."""
    faker = Faker()

    def setUp(self):
        self.speaker = Speaker.objects.create(name="Paul Ryan")
        self.speaker_profile_url = reverse(
            "speaker_profile",
            kwargs={"pk": self.speaker.pk, "slug": self.speaker.slug},
        )
        # Create base conference infrastructure.
        conference = Conference(title="Conference")
        conference.save()
        section = Section(
            conference=conference, name="Section", slug="section"
        )
        section.save()
        proposal_kind = ProposalKindFactory.create(section=section)
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
            reverse(
                "speaker_profile", args=[self.speaker.pk, self.speaker.slug]
            )
        )
        self.assertContains(response, FIRST_PRESENTATION_TITLE)
        self.assertContains(response, SECOND_PRESENTATION_TITLE)

    def test_do_not_display_unscheduled_presentations(self):
        self.second_presentation.slot = None
        self.second_presentation.save()

        response = self.client.get(
            reverse(
                "speaker_profile", args=[self.speaker.pk, self.speaker.slug]
            )
        )
        self.assertContains(response, FIRST_PRESENTATION_TITLE)
        self.assertNotContains(response, SECOND_PRESENTATION_TITLE)

    def test_second_speaker_profile_page(self):
        """Verify that a second speaker's profile page is public."""
        second_speaker = Speaker.objects.create(name="Nancy Pelosi")
        self.first_presentation.additional_speakers.add(second_speaker)

        response = self.client.get(
            reverse(
                "speaker_profile",
                args=[second_speaker.pk, second_speaker.slug],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, FIRST_PRESENTATION_TITLE)
        self.assertNotContains(response, SECOND_PRESENTATION_TITLE)

    def test_url_with_only_pk(self):
        response = self.client.get(
            reverse("speaker_profile_redirect", kwargs={"pk": self.speaker.pk})
        )
        self.assertRedirects(response, self.speaker_profile_url, 301)

    def test_url_with_pk_and_incorrect_slug(self):
        fuzzy_slug = self.faker.slug()
        response = self.client.get(
            reverse(
                "speaker_profile",
                kwargs={
                    "pk": self.speaker.pk,
                    "slug": fuzzy_slug,
                },
            )
        )
        self.assertRedirects(response, self.speaker_profile_url, 301)
