from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from symposion.schedule.tests.factories import ConferenceFactory


class ConferenceSiteAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@pydata.org',
            password='admin',
        )
        cls.conference = ConferenceFactory.create()
