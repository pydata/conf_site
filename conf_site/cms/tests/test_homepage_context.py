from django.test import TestCase
from django.urls import reverse

from symposion.conference.models import Conference
from wagtail.wagtailcore.models import Site

from conf_site.cms.models import HTMLPage, HomePage


class HomePageContextTestCase(TestCase):
    EXAMPLE_URL = "http://example.com"

    @classmethod
    def setUp(self):
        """Create Wagtail pages used in tests."""
        # The site needs a Conference to work properly.
        self.conference = Conference(title="Conference")
        self.conference.save()

        homepage = HomePage(title="Home",
                            path="0002",
                            depth=1,
                            ticketing_url=self.EXAMPLE_URL)
        homepage.save()
        # We need to replace the "Welcome to Wagtail" page with this page.
        site = Site.objects.get()
        site.root_page = homepage
        site.save()

        other_page = HTMLPage(title="Other",
                              path="0003")
        homepage.add_child(instance=other_page)
        other_page.save()

    def test_homepage_context(self):
        homepage = HomePage.objects.get()
        with self.settings(CONFERENCE_ID=self.conference.id):
            response = self.client.get(homepage.url)
        self.assertEqual(response.context["ticketing_url"], self.EXAMPLE_URL)

    def test_other_wagtail_page_context(self):
        other_page = HTMLPage.objects.get()
        response = self.client.get(other_page.url)
        self.assertEqual(response.context["ticketing_url"], self.EXAMPLE_URL)

    def test_symposion_page_context(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.context["ticketing_url"], self.EXAMPLE_URL)
