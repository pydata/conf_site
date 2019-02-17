# coding=utf-8
from bs4 import BeautifulSoup

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse

from symposion.reviews.models import ProposalResult, ResultNotification

from conf_site.proposals.tests import ProposalTestCase


GENERIC_EMAIL = "example@example.com"


class ProposalStatusTestCase(LiveServerTestCase, ProposalTestCase):
    """
    Test case to verify that proposals show the correct status to users.

    Users should see their proposals as "Submitted" unless their proposal
    has been accepted *and* they have been notified (in which case it
    should appear as "Accepted").

    """
    def setUp(self):
        super(ProposalStatusTestCase, self).setUp()
        # Create a ProposalResult for this proposal.
        self.proposal.result = ProposalResult.objects.create(
            proposal=self.proposal)
        self.proposal.result.save()

        # Create and login as a user associated with this test case's speaker.
        self.proposal.speaker.user = User.objects.create_user(
            username="user", email=GENERIC_EMAIL, password="asdf")
        self.proposal.speaker.save()
        self.client.login(
            username=self.proposal.speaker.user.email, password="asdf")

    def _notify(self):
        """Helper method to create proposal notification."""
        ResultNotification.objects.create(
            proposal=self.proposal,
            to_address=GENERIC_EMAIL,
            from_address=GENERIC_EMAIL,
            subject="",
            body="")

    def _change_status(self, new_status):
        """
        Helper method to modify a proposal's status.

        Due to the way the reviews application works, the status actually
        gets set on the proposal's ProposalResult object. ¯\_(ツ)_/¯

        """
        self.proposal.result.status = new_status
        self.proposal.result.save()

    def _get_dashboard_proposal_status(self):
        """Helper method to pull a proposal's status from dashboard page."""
        # Create a CSS selector that will give us the exact displayed status.
        proposal_status = "#proposal-{} .proposal-result-status .label".format(
            self.proposal.pk)

        response = self.client.get(reverse("dashboard"))
        # Use beautifulsoup to parse the response in order to find
        # the proposal's status on the page.
        parsed_response = BeautifulSoup(response.content, "html.parser")
        label = parsed_response.select(proposal_status)[0]
        return label.text

    def test_submitted_proposal_status(self):
        self._change_status("submitted")
        self.assertIs(self.proposal.notifications.count(), 0)
        self.assertEqual(self._get_dashboard_proposal_status(), "Submitted")

    def test_unnotified_accepted_proposal_status(self):
        self._change_status("accepted")
        self.assertIs(self.proposal.notifications.count(), 0)
        self.assertEqual(self._get_dashboard_proposal_status(), "Submitted")

    def test_unnotified_rejected_proposal_status(self):
        self._change_status("rejected")
        self.assertIs(self.proposal.notifications.count(), 0)
        self.assertEqual(self._get_dashboard_proposal_status(), "Submitted")

    def test_notified_accepted_proposal_status(self):
        self._change_status("accepted")
        self._notify()
        self.assertIsNot(self.proposal.notifications.count(), 0)
        self.assertEqual(self._get_dashboard_proposal_status(), "Accepted")

    def test_notified_rejected_proposal_status(self):
        self._change_status("rejected")
        self._notify()
        self.assertIsNot(self.proposal.notifications.count(), 0)
        self.assertEqual(self._get_dashboard_proposal_status(), "Submitted")
