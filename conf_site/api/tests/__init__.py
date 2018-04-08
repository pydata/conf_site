from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from symposion.conference.models import Conference


class ConferenceSiteAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.CONFERENCE_TITLE = "PyData"
        cls.CONFERENCE_START = "2040-01-01"
        cls.CONFERENCE_END = "2040-01-04"

        cls.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@pydata.org',
            password='admin',
        )
        cls.conference = Conference.objects.create(
            title=cls.CONFERENCE_TITLE,
            start_date=cls.CONFERENCE_START,
            end_date=cls.CONFERENCE_END
        )
