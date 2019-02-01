import random

from django.test import TestCase

from conf_site.sponsorship.tests import SponsorFactory
from conf_site.sponsorship.views import ExportSponsorsView


class ExportSponsorsViewTestCase(TestCase):
    def test_not_including_inactive_sponsor(self):
        """Verify that inactive sponsors are not included."""
        inactive_sponsor = SponsorFactory(active=False)
        response = ExportSponsorsView().get()
        self.assertNotContains(response, inactive_sponsor.name)

    def test_including_active_sponsors(self):
        """Verify that multiple sponsors are included."""
        sponsors = []
        for _ in range(random.randint(0, 5)):
            sponsors.append(SponsorFactory(active=True))
        response = ExportSponsorsView().get()
        for sponsor in sponsors:
            self.assertContains(response, sponsor.name)
            self.assertContains(response, sponsor.external_url)
            self.assertContains(response, sponsor.contact_name)
            self.assertContains(response, sponsor.contact_email)
            self.assertContains(response, sponsor.level)
