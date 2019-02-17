from django.test import TestCase
from django.urls import reverse


class CsrfFailureTestCase(TestCase):
    def test_access_csrf_failure_view(self):
        """Verify that custom CSRF failure view loads properly."""
        response = self.client.get(reverse("403-csrf"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403_csrf.html")
