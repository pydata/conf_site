# -*- coding: utf-8 -*-
from django.urls import reverse

from conf_site.schedule.tests import PresentationTestCase


class SchedulePresentationRedirectViewTestCase(PresentationTestCase):
    def test_url_with_only_pk(self):
        response = self.client.get(
            reverse(
                "schedule_presentation_redirect",
                kwargs={"pk": self.presentation.pk},
            )
        )
        self.assertRedirects(response, self.presentation_url, 301)
