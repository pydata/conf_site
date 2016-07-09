from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework import status
from symposion.speakers.models import Speaker

from .base import TestBase


class TestSpeaker(TestBase):

    @classmethod
    def setUpTestData(cls):
        super(TestSpeaker, cls).setUpTestData()
        cls.speaker = Speaker.objects.create(
            user=User.objects.create_user('test', 'test@pydata.org', 'test'),
            name='test speaker',
        )

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
        self.assertIn(
            {
                'username': self.speaker.user.username,
                'name': self.speaker.name,
                'email': self.speaker.user.email,
                'absolute_url': reverse('speaker_profile', args=[self.speaker.pk]),
            },
            response.data
        )

    def test_speaker_detail_api_admin_user(self):
        self.client.login(username='admin@pydata.org', password='admin')
        response = self.client.get(
            reverse('speaker-detail', args=[self.speaker.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                'username': self.speaker.user.username,
                'name': self.speaker.name,
                'email': self.speaker.user.email,
                'absolute_url': reverse('speaker_profile', args=[self.speaker.pk]),
            },
            response.data
        )
