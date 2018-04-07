import json

from django.core.urlresolvers import reverse

from rest_framework import status
from symposion.sponsorship.models import Sponsor, SponsorLevel

from conf_site.api.tests import ConferenceSiteAPITestCase


class ConferenceSiteAPISponsorTestCase(ConferenceSiteAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super(ConferenceSiteAPISponsorTestCase, cls).setUpTestData()

        # Create a sponsor.
        sponsor_level = SponsorLevel.objects.create(
            conference=cls.conference,
            name="Vibrantium",
            cost=42
        )
        # We don't use Sponsor.objects.create() here because it
        # fails with an IntegrityError.
        cls.sponsor = Sponsor(
            name="FooBar Inc.",
            external_url="http://example.com",
            contact_name="Foo Bar",
            contact_email="foobar@example.com",
            level=sponsor_level,
            active=True,
        )
        cls.sponsor.save()

    def test_sponsor_list_api_anonymous_user(self):
        """Verify that anonymous users cannot access list of sponsors."""
        response = self.client.get(reverse('sponsor-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sponsor_list_api_admin_user(self):
        """Verify that admin users can access list of sponsors."""
        self.client.login(username="admin@pydata.org", password="admin")
        response = self.client.get(reverse("sponsor-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            {
                'name': self.sponsor.name,
                'external_url': self.sponsor.external_url,
                'contact_name': self.sponsor.contact_name,
                'contact_email': self.sponsor.contact_email,
                'level': {'name': self.sponsor.level.name,
                          'cost': self.sponsor.level.cost},
                'absolute_url': (
                    'http://testserver' + self.sponsor.get_absolute_url()),
                'annotation': self.sponsor.annotation,
            },
            json.loads(response.content)
        )

    def test_sponsor_detail_api_anonymous_user(self):
        """Verify that anonymous users cannot access sponsor details."""
        response = self.client.get(
            reverse('sponsor-detail', args=[self.sponsor.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sponsor_detail_api_admin_user(self):
        """Verify that admin users can access sponsor details."""
        self.client.login(username="admin@pydata.org", password="admin")
        response = self.client.get(
            reverse('sponsor-detail', args=[self.sponsor.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                'name': self.sponsor.name,
                'external_url': self.sponsor.external_url,
                'contact_name': self.sponsor.contact_name,
                'contact_email': self.sponsor.contact_email,
                'level': {'name': self.sponsor.level.name,
                          'cost': self.sponsor.level.cost},
                'absolute_url': (
                    'http://testserver' + self.sponsor.get_absolute_url()),
                'annotation': self.sponsor.annotation,
            },
            json.loads(response.content)
        )
