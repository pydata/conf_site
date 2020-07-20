# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Site
from wagtail.core.rich_text import RichText

from conf_site.schedule.models import ScheduleSettings


class ScheduleSettingsTestCase(TestCase):
    def setUp(self):
        super(ScheduleSettingsTestCase, self).setUp()

        self.settings = ScheduleSettings.for_site(
            Site.objects.get(is_default_site=True)
        )

    def test_legend_display(self):
        """Verify that the legend appears if set."""
        new_legend = "<h3>ZELDA</h3>"
        self.settings.legend = [('rich_text', RichText(new_legend))]
        self.settings.save()

        response = self.client.get(reverse("schedule_conference"))
        self.assertContains(response, new_legend)
        self.assertNotContains(response, "<p>View past PyData event schedules")
