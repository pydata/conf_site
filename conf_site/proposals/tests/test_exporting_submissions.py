from random import randint

from conf_site.core.tests.test_csv_view import StaffOnlyCsvViewTestCase
from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.proposals.views import ExportSubmissionsView


class ExportSubmissionsViewTestCase(StaffOnlyCsvViewTestCase):
    view_class = ExportSubmissionsView
    view_name = "submission_export"

    def test_all_proposals_are_included(self):
        proposals = ProposalFactory.create_batch(size=randint(2, 4))
        response = ExportSubmissionsView().get()
        for proposal in proposals:
            self.assertContains(response, proposal.speaker.name)
            self.assertContains(response, proposal.title)
            self.assertContains(response, proposal.affiliation)
            self.assertContains(response, proposal.code_url)
            self.assertContains(response, proposal.kind.name)
