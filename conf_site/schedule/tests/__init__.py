# -*- coding: utf-8 -*-
from django.urls import reverse

from conf_site.proposals.tests import ProposalTestCase
from conf_site.schedule.tests.factories import PresentationFactory


class PresentationTestCase(ProposalTestCase):
    def setUp(self):
        super().setUp()
        self.presentation = PresentationFactory()
        self.presentation_url = reverse(
            "schedule_presentation_detail",
            kwargs={
                "pk": self.presentation.pk,
                "slug": self.presentation.slug,
            },
        )
