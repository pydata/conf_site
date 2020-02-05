from conf_site.core.tests.test_csv_view import CsvViewTestCase
from conf_site.schedule.views import ExportPresentationSpeakerView


class ExportPresentationSpeakerViewTestCase(CsvViewTestCase):
    view_class = ExportPresentationSpeakerView
