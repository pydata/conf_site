from django.urls import reverse

from conf_site.core.tests.test_csv_view import StaffOnlyCsvViewTestCase
from conf_site.schedule.tests.factories import PresentationFactory
from conf_site.schedule.views import ExportPresentationSpeakerView


class ExportPresentationSpeakerViewTestCase(StaffOnlyCsvViewTestCase):
    view_class = ExportPresentationSpeakerView
    view_name = "presentation_speaker_export"

    def test_cancelled_presentations_do_not_appear(self):
        self._become_staff()
        self.client.login(username=self.user.email, password=self.password)

        cancelled_presentation = PresentationFactory(cancelled=True)
        response = self.client.get(reverse(self.view_name))
        self.assertNotContains(response, cancelled_presentation.title)
