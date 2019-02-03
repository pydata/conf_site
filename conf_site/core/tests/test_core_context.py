from django.core.urlresolvers import reverse
from django.test import TestCase


class CoreContextProcessorTestCase(TestCase):
    def test_google_analytics_id(self):
        """Verify that Google Analytics ID appears in the context & HTML."""
        GA_EXAMPLE_ID = "UA-1234567-88"
        with self.settings(GOOGLE_ANALYTICS_PROPERTY_ID=GA_EXAMPLE_ID):
            # This URL shouldn't matter - all pages should have GA information.
            response = self.client.get(reverse("account_login"))
            self.assertEqual(
                response.context.get("google_analytics_id"), GA_EXAMPLE_ID
            )
            self.assertContains(response, GA_EXAMPLE_ID)

    def test_sentry_public_dsn(self):
        """Verify that the Sentry public DSN appears in context & HTML."""
        SENTRY_PUBLIC_DSN = "https://SUPERB@sentry.io/OWL"
        with self.settings(SENTRY_PUBLIC_DSN=SENTRY_PUBLIC_DSN):
            response = self.client.get(reverse("account_login"))
            self.assertEqual(
                response.context.get("sentry_public_dsn"), SENTRY_PUBLIC_DSN
            )
            self.assertContains(response, SENTRY_PUBLIC_DSN)
