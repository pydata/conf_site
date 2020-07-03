from django.urls import reverse

from rest_framework import status

from conf_site.api.tests import ConferenceSiteAPITestCase
from conf_site.sponsorship.tests import SponsorFactory


class ConferenceSiteAPISponsorTestCase(ConferenceSiteAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super(ConferenceSiteAPISponsorTestCase, cls).setUpTestData()

        # Create a sponsor.
        cls.sponsor = SponsorFactory.create(active=True)
        cls.sponsor.save()

        # Create sponsor dict to avoid duplication.
        cls.sponsor_dict = {
            "name": cls.sponsor.name,
            "external_url": cls.sponsor.external_url,
            "contact_name": cls.sponsor.contact_name,
            "contact_email": cls.sponsor.contact_email,
            "level": {"name": cls.sponsor.level.name,
                      "cost": cls.sponsor.level.cost},
            "absolute_url": (
                "http://testserver" + cls.sponsor.get_absolute_url()),
            "annotation": cls.sponsor.annotation,
        }

    def test_sponsor_list_api_anonymous_user(self):
        """Verify that anonymous users cannot access list of sponsors."""
        response = self.client.get(reverse('sponsor-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sponsor_list_api_admin_user(self):
        """Verify that admin users can access list of sponsors."""
        self.client.login(username="admin@pydata.org", password="admin")
        response = self.client.get(reverse("sponsor-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.sponsor_dict, response.json())

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
        self.assertEqual(self.sponsor_dict, response.json())
