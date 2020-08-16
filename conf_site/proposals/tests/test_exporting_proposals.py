# -*- coding: utf-8 -*-
from random import randint

from conf_site.core.tests.test_csv_view import StaffOnlyCsvViewTestCase
from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.proposals.views import ExportProposalsView


class ExportProposalsViewTestCase(StaffOnlyCsvViewTestCase):
    view_class = ExportProposalsView
    view_name = "proposal_export"

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

    def test_include_cancelled_proposal_status(self):
        proposal = ProposalFactory.create(cancelled=True)
        response = ExportProposalsView().get()
        self.assertContains(response, proposal.title)
        self.assertContains(response, "Cancelled")
