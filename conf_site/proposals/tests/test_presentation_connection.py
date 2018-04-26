from symposion.conference.models import Section
from symposion.proposals.models import ProposalBase
from symposion.schedule.models import Presentation

from conf_site.proposals.tests import ProposalTestCase


class PresentationProposalConnectionTestCase(ProposalTestCase):
    def test_presentation_proposal_model(self):
        """Make sure presentation.proposal is Proposal, not ProposalBase."""
        # Create Presentation connected to existing Proposal.
        proposal_base = ProposalBase.objects.get(
            title=self.proposal.title,
            description=self.proposal.description,
            abstract=self.proposal.abstract,
            speaker=self.proposal.speaker,
        )
        presentation = Presentation.objects.create(
            title=self.proposal.title,
            description=self.proposal.description,
            abstract=self.proposal.abstract,
            speaker=self.proposal.speaker,
            section=Section.objects.first(),
            proposal_base=proposal_base,
        )
        # This should be a Proposal, not a ProposalBase.
        self.assertIs(type(presentation.proposal), type(self.proposal))
