from django.test import TestCase

from symposion.conference.models import Conference, Section
from symposion.proposals.models import ProposalKind
from symposion.schedule.models import Presentation
from symposion.speakers.models import Speaker

from conf_site.proposals.models import Proposal


class SaveProposalTestCase(TestCase):
    def setUp(self):
        # Create base conference infrastructure that has to exist in
        # order to create a Proposal.
        conference = Conference(title="Conference")
        conference.save()
        section = Section(
            conference=conference, name="Section", slug="section")
        section.save()
        proposal_kind = ProposalKind(section=section, name="Kind", slug="kind")
        proposal_kind.save()
        speaker = Speaker(name="Paul Ryan")
        speaker.save()
        self.proposal = Proposal(
            title="Title",
            description="Description",
            abstract="Abstract",
            kind=proposal_kind,
            speaker=speaker,
            audience_level=1,
        )

    def test_saving_proposal_without_presentation(self):
        """Verify that the proposal's overloaded save method works."""
        self.proposal.save()
        self.assertIsNotNone(self.proposal.pk)

    def test_saving_proposal_with_presentation(self):
        """Verify that saving a proposal updates its presentation."""
        # Save the proposal, so that it has a ProposalBase, which is
        # necessary to use M2M relationships like additional_speakers.
        self.proposal.save()
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
