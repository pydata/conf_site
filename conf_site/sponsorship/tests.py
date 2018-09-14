from django.conf import settings
from django.urls import reverse

from symposion.conference.models import Conference

from wagtail.wagtailcore.models import Site

from conf_site.accounts.tests import AccountsTestCase
from conf_site.sponsorship.models import SponsorshipSettings


# We inherit from AccountsTestCase because we need a User for sponsor_apply.
class SponsorshipSettingsTestCase(AccountsTestCase):
    def setUp(self):
        super(SponsorshipSettingsTestCase, self).setUp()

        self.conference = Conference.objects.get_or_create(
            pk=settings.CONFERENCE_ID, title="Conference"
        )[0]

        self.settings = SponsorshipSettings.for_site(
            Site.objects.get(is_default_site=True)
        )
        self.default_info_link = SponsorshipSettings._meta.get_field(
            "info_link"
        ).default

    def test_default_info_link(self):
        """Ensure that default info_link URL appears in relevant templates."""

        response = self.client.get(reverse("sponsor_list"))
        self.assertContains(response, self.default_info_link)

        self.client.force_login(self.user)

        response = self.client.get(reverse("sponsor_apply"))
        self.assertContains(response, self.default_info_link)

    def test_modifying_info_link(self):
        """Ensure that changing info_link also changes templates."""
        new_info_link = "http://example.com/sponsor/info/"
        self.settings.info_link = new_info_link
        self.settings.save()

        response = self.client.get(reverse("sponsor_list"))
        self.assertContains(response, new_info_link)
        self.assertNotContains(response, self.default_info_link)

        self.client.force_login(self.user)

        response = self.client.get(reverse("sponsor_apply"))
        self.assertContains(response, new_info_link)
        self.assertNotContains(response, self.default_info_link)
