from symposion.schedule.models import Presentation

from conf_site.proposals.tests import ProposalTestCase


class SaveProposalTestCase(ProposalTestCase):
    def test_saving_proposal_without_presentation(self):
        """Verify that the proposal's overloaded save method works."""
        self.assertIsNotNone(self.proposal.pk)

    def test_saving_proposal_with_presentation(self):
        """Verify that saving a proposal updates its presentation."""
        presentation = Presentation()
        self.proposal.presentation = presentation
        # Save the proposal again, so that the presentation will be
        # saved as well.
        self.proposal.save()
        self.assertEqual(self.proposal.title, presentation.title)
        self.assertEqual(self.proposal.description, presentation.description)
        self.assertEqual(self.proposal.abstract, presentation.abstract)
        self.assertEqual(self.proposal.speaker, presentation.speaker)
        self.assertEqual(self.proposal.kind.section, presentation.section)
