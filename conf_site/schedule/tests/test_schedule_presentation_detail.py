# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.urls import reverse

from faker import Faker

from conf_site.schedule.tests import PresentationTestCase


class SchedulePresentationDetailViewTestCase(PresentationTestCase):
    faker = Faker()

    def _unpublish_schedule(self):
        """Utility method to unpublish associated presentation's schedule."""
        schedule = self.presentation.slot.day.schedule
        schedule.published = False
        schedule.save()

    def test_status_code(self):
        """Verify that presentation page returns a 200 status code."""

        response = self.client.get(self.presentation_url)
        self.assertEqual(response.status_code, 200)

    def test_unpublished_schedule(self):
        """
        Verify that presentation pages do not work
        when schedule is unpublished.
        """
        self._unpublish_schedule()
        response = self.client.get(self.presentation_url)
        self.assertEqual(response.status_code, 404)

    def test_unpublished_schedule_with_staff(self):
        """
        Verify that presentation pages work
        when schedule is unpublished, but
        requesting user is staff.
        """
        self._unpublish_schedule()

        # Create a staff user and login as them.
        password = self.faker.sentence(nb_words=6)
        user_model = get_user_model()
        user = user_model.objects.create(
            username="test",
            email="example@example.com",
            first_name="Test",
            last_name="User",
            is_staff=True,
        )
        user.set_password(password)
        user.save()
        self.client.force_login(user)

        response = self.client.get(self.presentation_url)
        self.assertEqual(response.status_code, 200)

    def test_url_with_pk_and_incorrect_slug(self):
        fuzzy_slug = self.faker.slug()
        response = self.client.get(
            reverse(
                "schedule_presentation_detail",
                kwargs={
                    "pk": self.presentation.pk,
                    "slug": fuzzy_slug,
                },
            )
        )
        self.assertRedirects(response, self.presentation_url, 301)
