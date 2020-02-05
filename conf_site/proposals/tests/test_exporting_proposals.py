# -*- coding: utf-8 -*-
from random import randint

from django.urls import reverse

from conf_site.accounts.tests import AccountsTestCase
from conf_site.core.tests.test_csv_view import CsvViewTestCase
from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.proposals.views import ExportProposalsView


class ExportProposalsViewTestCase(AccountsTestCase, CsvViewTestCase):
    view_class = ExportProposalsView

    def test_all_proposals_are_included(self):
        proposals = ProposalFactory.create_batch(size=randint(2, 4))
        response = ExportProposalsView().get()
        for proposal in proposals:
            self.assertContains(response, proposal.number)
            self.assertContains(response, proposal.title)
            self.assertContains(response, proposal.speaker.name)
            self.assertContains(response, proposal.kind.name)
            self.assertContains(
                response, proposal.get_audience_level_display()
            )
            self.assertContains(response, proposal.date_created)
            self.assertContains(response, proposal.date_last_modified)

    def test_no_anonymous_access(self):
        self.client.logout()
        response = self.client.get(reverse("proposal_export"))
        self.assertEqual(response.status_code, 302)

    def test_staff_access(self):
        self._become_staff()
        self.client.login(username=self.user.email, password=self.password)
        response = self.client.get(reverse("proposal_export"))
        self.assertEqual(response.status_code, 200)
