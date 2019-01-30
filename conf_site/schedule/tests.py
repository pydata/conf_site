from django.test import TestCase
from django.urls import reverse

from wagtail.wagtailcore.models import Site
from wagtail.wagtailcore.rich_text import RichText

from conf_site.schedule.models import ScheduleSettings
from conf_site.schedule.views import ExportPresentationSpeakerView


class ScheduleSettingsTestCase(TestCase):
    def setUp(self):
        super(ScheduleSettingsTestCase, self).setUp()

        self.settings = ScheduleSettings.for_site(
            Site.objects.get(is_default_site=True)
        )

    def test_no_legend_set(self):
        """Verify that default text appears if no custom legend is set."""
        response = self.client.get(reverse("schedule_conference"))
        self.assertContains(response, "<p>View past PyData event schedules")

    def test_legend_display(self):
        """Verify that the legend appears if set."""
        new_legend = "<h3>ZELDA</h3>"
        self.settings.legend = [('rich_text', RichText(new_legend))]
        self.settings.save()

        response = self.client.get(reverse("schedule_conference"))
        self.assertContains(response, new_legend)
        self.assertNotContains(response, "<p>View past PyData event schedules")


class ExportPresentationSpeakerViewTestCase(TestCase):
    def test_status_code(self):
        response = ExportPresentationSpeakerView().get()
        self.assertEqual(response.status_code, 200)
