import glob

from django.contrib.auth.models import User
from django.core.management import call_command

from rest_framework.test import APITestCase


class TestBase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@pydata.org',
            password='admin',
        )
        call_command('loaddata', *glob.glob('fixtures/*'))
