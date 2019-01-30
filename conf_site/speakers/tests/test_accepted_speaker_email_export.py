from django.test import TestCase

from conf_site.speakers.views import ExportAcceptedSpeakerEmailView


class ExportAcceptedSpeakerEmailViewTestCase(TestCase):
    def test_status_code(self):
        response = ExportAcceptedSpeakerEmailView().get()
        self.assertEqual(response.status_code, 200)
