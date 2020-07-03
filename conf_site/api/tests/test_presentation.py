from django.urls import reverse

from rest_framework import status

from conf_site.api.tests import ConferenceSiteAPITestCase
from conf_site.schedule.tests.factories import PresentationFactory
from conf_site.speakers.tests.factories import SpeakerFactory
from symposion.schedule.tests.factories import ScheduleFactory


class ConferenceSiteAPISponsorTestCase(ConferenceSiteAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super(ConferenceSiteAPISponsorTestCase, cls).setUpTestData()
        cls.speaker = SpeakerFactory.create()
        cls.schedule = ScheduleFactory.create()
        cls.presentation = PresentationFactory.create()

    def test_presentation_list_api_anonymous_user(self):
        response = self.client.get(reverse('presentation-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_presentation_list_api_admin_user(self):
        self.client.login(username='admin@pydata.org', password='admin')
        response = self.client.get(reverse('presentation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_presentation_detail_api_anonymous_user(self):
        response = self.client.get(
            reverse('presentation-detail', args=[self.presentation.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_presentation_detail_api_admin_user(self):
        self.client.login(username='admin@pydata.org', password='admin')
        response = self.client.get(
            reverse('presentation-detail', args=[self.presentation.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
