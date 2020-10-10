from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from conf_site.schedule.tests.factories import PresentationFactory
from symposion.conference.models import Conference, Section
from symposion.schedule.models import Schedule
from symposion.schedule.tests.factories import SlotFactory, SlotKindFactory


class ScheduleListCSVViewTestCase(TestCase):
    """Automated test cases for the schedule_list_csv view."""

    @classmethod
    def setUpTestData(cls):
        super(ScheduleListCSVViewTestCase, cls).setUpTestData()

        CONFERENCE_TITLE = "PyData"
        CONFERENCE_START = "2040-01-01"
        CONFERENCE_END = "2040-01-04"

        conference = Conference.objects.create(
            title=CONFERENCE_TITLE,
            start_date=CONFERENCE_START,
            end_date=CONFERENCE_END,
        )
        section = Section.objects.create(
            name="FooBarSection", slug="foo-bar", conference=conference
        )
        cls.schedule = Schedule.objects.create(section=section)

    def _unpublish_schedule(self):
        self.schedule.published = False
        self.schedule.save()

    def test_404_if_schedule_is_unpublished(self):
        self._unpublish_schedule()

        response = self.client.get(reverse("schedule_list_csv"))
        self.assertEqual(response.status_code, 404)

    def test_200_if_user_is_staff(self):
        """Verify unpublished schedule CSV displays to staff users."""
        TEST_USERNAME = "test_user"
        TEST_EMAIL = "example@example.com"
        TEST_PASSWORD = "b4nd3rsn4tch"

        self._unpublish_schedule()
        # Create and login as a staff user.
        User.objects.create_user(
            username=TEST_USERNAME,
            email=TEST_EMAIL,
            password=TEST_PASSWORD,
            is_staff=True,
        )
        self.assertTrue(
            self.client.login(username=TEST_EMAIL, password=TEST_PASSWORD)
        )

        response = self.client.get(reverse("schedule_list_csv"))
        self.assertEqual(response.status_code, 200)

    def test_no_cancelled_presentations(self):
        self.schedule.published = True
        self.schedule.save()
        cancelled_presentation = PresentationFactory(
            cancelled=True,
            slot=SlotFactory(kind=SlotKindFactory(schedule=self.schedule)),
        )
        response = self.client.get(
            reverse("schedule_list_csv", args=[self.schedule.section.slug])
        )
        self.assertNotContains(response, cancelled_presentation.title)
