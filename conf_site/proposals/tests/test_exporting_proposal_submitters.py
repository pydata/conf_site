# -*- coding: utf-8 -*-
from random import randint

from django.urls import reverse

from conf_site.accounts.tests import AccountsTestCase
from conf_site.core.tests.test_csv_view import CsvViewTestCase
from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.proposals.views import ExportProposalSubmittersView
from conf_site.speakers.tests.factories import SpeakerFactory


class ExportProposalSubmittersViewTestCase(AccountsTestCase, CsvViewTestCase):
    view_class = ExportProposalSubmittersView

    def test_header_row(self):
        """Verify that header row appears in CSV file response."""
        view = ExportProposalSubmittersView()
        response = view.get()
        # Some formatting needs to be done so that the header row
        # is compliant with the CSV dialect - all fields need
        # to be quoted.
        quoted_header_row = "\"{}\"".format("\",\"".join(view.header_row))
        self.assertContains(response, quoted_header_row)

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

    def test_no_anonymous_access(self):
        self.client.logout()
        response = self.client.get(reverse("proposal_submitter_export"))
        self.assertEqual(response.status_code, 302)

    def test_staff_access(self):
        self._become_staff()
        self.client.login(username=self.user.email, password=self.password)
        response = self.client.get(reverse("proposal_submitter_export"))
        self.assertEqual(response.status_code, 200)
