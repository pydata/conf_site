from django.core.files.images import ImageFile
from django.test import override_settings, TestCase
from django.urls import reverse

from faker import Faker
from symposion.conference.models import Conference
from wagtail.core.models import Site
from wagtail.images import get_image_model

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

    @override_settings(
        STATICFILES_STORAGE=(
            "django.contrib.staticfiles.storage.StaticFilesStorage"
        )
    )
    def test_logo_image(self):
        homepage = HomePage.objects.get()
        self.assertIsNone(homepage.logo_image)
        with self.settings(CONFERENCE_ID=self.conference.id):
            # Test that default logo image appears.
            response = self.client.get(homepage.url)
            self.assertContains(response, "/logo.png")
            # Replace default logo with a new image.
            test_logo_name = Faker().uuid4()
            image_file = ImageFile(
                open("conf_site/cms/tests/test-logo.png", "rb"), test_logo_name
            )
            ImageModel = get_image_model()
            image = ImageModel(file=image_file)
            # The image must be saved before it is attached
            # to the homepage.
            image.save()
            homepage.logo_image = image
            homepage.save()
            response = self.client.get(homepage.url)
            self.assertNotContains(response, "/logo.288981a8dfa8.png")
            self.assertContains(response, test_logo_name)
