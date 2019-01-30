from django.test import TestCase

from conf_site.core.views import CsvView


class CsvViewTestCase(TestCase):
    def test_response_mimetype(self):
        """Verify that response's mimetype is a CSV."""
        response = CsvView().get()
        self.assertTrue(response.has_header("Content-Type"))
        self.assertEqual(response.__getitem__("Content-Type"), "text/csv")
