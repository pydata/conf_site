from conf_site.core.tests.test_csv_view import CsvViewTestCase
from conf_site.speakers.views import ExportAcceptedSpeakerEmailView


class ExportAcceptedSpeakerEmailViewTestCase(CsvViewTestCase):
    view_class = ExportAcceptedSpeakerEmailView
