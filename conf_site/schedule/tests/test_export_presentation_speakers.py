from conf_site.core.tests.test_csv_view import StaffOnlyCsvViewTestCase
from conf_site.schedule.views import ExportPresentationSpeakerView


class ExportPresentationSpeakerViewTestCase(StaffOnlyCsvViewTestCase):
    view_class = ExportPresentationSpeakerView
    view_name = "presentation_speaker_export"
