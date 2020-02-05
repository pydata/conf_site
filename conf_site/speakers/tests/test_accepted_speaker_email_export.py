from conf_site.core.tests.test_csv_view import StaffOnlyCsvViewTestCase
from conf_site.speakers.views import ExportAcceptedSpeakerEmailView


class ExportAcceptedSpeakerEmailViewTestCase(StaffOnlyCsvViewTestCase):
    view_class = ExportAcceptedSpeakerEmailView
    view_name = "speaker_email_export"
