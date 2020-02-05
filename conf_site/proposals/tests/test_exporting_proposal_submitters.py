# -*- coding: utf-8 -*-
from random import randint

from conf_site.core.tests.test_csv_view import StaffOnlyCsvViewTestCase
from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.proposals.views import ExportProposalSubmittersView
from conf_site.speakers.tests.factories import SpeakerFactory


class ExportProposalSubmittersViewTestCase(StaffOnlyCsvViewTestCase):
    view_class = ExportProposalSubmittersView
    view_name = "proposal_submitter_export"

    def test_all_proposals_are_included(self):
        proposals = ProposalFactory.create_batch(size=randint(2, 4))
        response = ExportProposalSubmittersView().get()
        for proposal in proposals:
            self.assertContains(response, proposal.speaker.name)
            self.assertContains(response, proposal.speaker.email)
            self.assertContains(response, proposal.title)

    def test_additional_speakers_are_included(self):
        """Verify that we are picking up both types of speakers."""
        proposal = ProposalFactory()
        additional_speakers = SpeakerFactory.create_batch(size=randint(2, 4))
        proposal.additional_speakers.add(*additional_speakers)
        response = ExportProposalSubmittersView().get()
        for speaker in additional_speakers:
            self.assertContains(response, speaker.name)
            self.assertContains(response, speaker.email)
