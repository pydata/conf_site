from django.test import TestCase
from django.urls import reverse

from conf_site.accounts.tests import AccountsTestCase
from conf_site.core.views import CsvView


class CsvViewTestCase(TestCase):
    view_class = CsvView

    def test_status_code(self):
        response = self.view_class().get()
        self.assertEqual(response.status_code, 200)

    def test_response_mimetype(self):
        """Verify that response's mimetype is a CSV."""
        response = CsvView().get()
        self.assertTrue(response.has_header("Content-Type"))
        self.assertEqual(response.__getitem__("Content-Type"), "text/csv")

    def test_header_row(self):
        """Verify that header row appears in CSV file response."""
        header_row = self.view_class().header_row
        if not header_row:
            return

        response = self.view_class().get()
        # Some formatting needs to be done so that the header row
        # is compliant with the CSV dialect - all fields need
        # to be quoted.
        quoted_header_row = '"{}"'.format('","'.join(header_row))
        self.assertContains(response, quoted_header_row)


class StaffOnlyCsvViewTestCase(AccountsTestCase, CsvViewTestCase):
    view_name = None

    def test_no_anonymous_access(self):
        if not self.view_name:
            return

        self.client.logout()
        response = self.client.get(reverse(self.view_name))
        self.assertEqual(response.status_code, 302)

    def test_staff_access(self):
        if not self.view_name:
            return

        self._become_staff()
        self.client.login(username=self.user.email, password=self.password)
        response = self.client.get(reverse(self.view_name))
        self.assertEqual(response.status_code, 200)
