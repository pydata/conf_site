from django.core.urlresolvers import reverse
from django.test import TestCase

from symposion.schedule.tests.factories import SlotFactory


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
