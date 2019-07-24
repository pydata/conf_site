# -*- coding: utf-8 -*-
from django.test import TestCase

from conf_site.schedule.views import ExportPresentationSpeakerView


class ExportPresentationSpeakerViewTestCase(TestCase):
    def test_status_code(self):
        response = ExportPresentationSpeakerView().get()
        self.assertEqual(response.status_code, 200)
