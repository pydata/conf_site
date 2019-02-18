from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from symposion.proposals.models import ProposalBase
from symposion.schedule.models import Presentation
from symposion.schedule.tests.factories import (
    SectionFactory, ProposalKindFactory, SlotFactory
)
from symposion.speakers.models import Speaker


class ScheduleJSONViewTestCase(TestCase):
    """Automated test cases for schedule_json view."""

    def test_empty_schedule(self):
        """Verify that an empty schedule returns empty JSON."""
        response = self.client.get(reverse("schedule_json"))
        # The JSON should contain an empty element named "schedule".
        self.assertContains(
            response=response, text="schedule", status_code=200
        )
        self.assertEqual(len(response.json()["schedule"]), 0)

    def test_presentation_count(self):
        PRESENTATION_COUNT = 5

        SlotFactory.create_batch(size=PRESENTATION_COUNT)

        response = self.client.get(reverse("schedule_json"))
        self.assertEqual(len(response.json()["schedule"]), PRESENTATION_COUNT)

    def test_slot_override(self):
        """Verify that slot.content_override displays in JSON."""
        OVERRIDDEN_CONTENT = "**FOOBAR**"

        slot = SlotFactory()
        slot.content_override = OVERRIDDEN_CONTENT
        slot.save()

        response = self.client.get(reverse("schedule_json"))
        self.assertContains(
            response=response, text=OVERRIDDEN_CONTENT, status_code=200
        )

    def test_presentation_data(self):
        """Verify that a presentation's content appears."""
        TALK_TITLE = "Presentation Content Verification Testing for Snakes"
        DESCRIPTION_CONTENT = "It was a bright cold day in April..."
        ABSTRACT_CONTENT = "...the color of television tuned to a dead channel"

        user_model = get_user_model()
        user = user_model.objects.create(
            username="test",
            email="example@example.com",
            first_name="Test",
            last_name="User",
        )
        speaker = Speaker.objects.create(user=user, name="Speaker")
        section = SectionFactory()
        proposal_kind = ProposalKindFactory()
        # We don't use factories so that all title/description/abstract
        # information is synchronized between the ProposalBase and the
        # Presentation.
        proposal_base = ProposalBase.objects.create(
            title=TALK_TITLE,
            description=DESCRIPTION_CONTENT,
            abstract=ABSTRACT_CONTENT,
            speaker=speaker,
            kind=proposal_kind,
        )
        presentation = Presentation.objects.create(
            title=TALK_TITLE,
            description=DESCRIPTION_CONTENT,
            abstract=ABSTRACT_CONTENT,
            speaker=speaker,
            proposal_base=proposal_base,
            section=section,
        )
        slot = SlotFactory()
        slot.assign(presentation)

        response = self.client.get(reverse("schedule_json"))
        self.assertContains(response=response, text=TALK_TITLE)
        self.assertContains(response=response, text=DESCRIPTION_CONTENT)
        self.assertContains(response=response, text=ABSTRACT_CONTENT)
