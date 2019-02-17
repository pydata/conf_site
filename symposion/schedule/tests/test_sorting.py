import datetime

from django.test import TestCase
from django.urls import reverse

from symposion.conference.models import Conference, Section
from symposion.schedule.models import Day, Schedule


class ScheduleSortingTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create a Conference and two Sections."""
        conference = Conference.objects.create(title="Conference")
        cls.section1 = Section.objects.create(
            conference=conference,
            name="Section AAAAA",
            slug="aaaaa",
            start_date=datetime.datetime(2000, 1, 1),
        )
        cls.section2 = Section.objects.create(
            conference=conference,
            name="Section BBBBB",
            slug="bbbbb",
            start_date=datetime.datetime(2010, 1, 1),
        )

    def test_default_ordering(self):
        """Verify that default sorting is by section start dates."""
        # We create schedule2 before schedule1 so that we can be
        # sure that the objects are not being sorted by ID.
        schedule2 = Schedule.objects.create(section=self.section2)
        schedule1 = Schedule.objects.create(section=self.section1)
        self.assertListEqual(
            list(Schedule.objects.all()), [schedule1, schedule2]
        )

    def test_schedule_conference_is_ordered_by_days(self):
        """Verify that schedule_conference view is sorting by first day."""
        schedule1 = Schedule.objects.create(
            section=self.section1, published=True
        )
        Day.objects.create(schedule=schedule1, date=datetime.date(2010, 1, 1))
        schedule2 = Schedule.objects.create(
            section=self.section2, published=True
        )
        Day.objects.create(schedule=schedule2, date=datetime.date(2000, 1, 1))
        # Ensure that schedule1's first date is later in time than schedule2's.
        self.assertGreater(schedule1.first_date(), schedule2.first_date())

        response = self.client.get(reverse("schedule_conference"))
        self.assertEqual(
            response.context["sections"][0]["schedule"], schedule2
        )
        self.assertEqual(
            response.context["sections"][1]["schedule"], schedule1
        )
