from django.core.urlresolvers import reverse

from rest_framework import status

from .base import TestBase


class TestConference(TestBase):

    def test_conference_api_anonymous_user(self):
        response = self.client.get(reverse('conference-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'title': 'PyData',
            'start_date': '2040-01-01',
            'end_date': '2040-01-04',
        })
