from django.urls import reverse

from rest_framework import status

from conf_site.api.tests import ConferenceSiteAPITestCase
from conf_site.speakers.tests.factories import SpeakerFactory


class TestSpeaker(ConferenceSiteAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super(TestSpeaker, cls).setUpTestData()
        cls.speaker = SpeakerFactory.create()
        cls.speaker_dict = {
            "username": cls.speaker.user.username,
            "name": cls.speaker.name,
            "email": cls.speaker.user.email,
            "absolute_url": "http://testserver" + reverse(
                "speaker_profile", args=[cls.speaker.pk, cls.speaker.slug]
            ),
        }

    def test_speaker_list_api_anonymous_user(self):
        response = self.client.get(reverse('speaker-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_speaker_list_api_speaker_user(self):
        self.client.login(username='test@pydata.org', password='test')
        response = self.client.get(reverse('speaker-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_speaker_list_api_admin_user(self):
        self.client.login(username='admin@pydata.org', password='admin')
        response = self.client.get(reverse('speaker-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.speaker_dict, response.json())

    def test_speaker_detail_api_admin_user(self):
        self.client.login(username='admin@pydata.org', password='admin')
        response = self.client.get(
            reverse('speaker-detail', args=[self.speaker.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.speaker_dict, response.json())
