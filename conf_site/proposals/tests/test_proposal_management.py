from django.urls import reverse

from conf_site.proposals.tests import ProposalSpeakerTestCase
from symposion.speakers.models import Speaker


class ProposalSpeakerManageViewTestCase(ProposalSpeakerTestCase):
    """Automated test cases for symposion's proposal_speaker_manage view."""

    INVITE_DUPLICATE_MESSAGE = (
        "This email address has already been invited to your talk proposal"
    )
    INVITE_SELF_MESSAGE = "You can&#39;t invite yourself to this proposal"
    INVITE_SUCCESS_MESSAGE = "Speaker invited to proposal."

    def setUp(self):
        super().setUp()

    def test_verify_proposal_jacking_does_not_work(self):
        """Verify that you can't manage a proposal that is not yours."""
        # Create a new speaker and change ownership of this
        # test case's Proposal to said speaker.
        other_speaker = Speaker.objects.create(name=self.faker.name())
        self.proposal.speaker = other_speaker
        self.proposal.save()

        response = self.client.get(
            reverse("proposal_speaker_manage", args=[self.proposal.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_inviting_speaker(self):
        """Verify that inviting a speaker works, but only the first time."""
        invite_email = self.faker.email()
        response = self.client.post(
            path=reverse("proposal_speaker_manage", args=[self.proposal.pk]),
            data={"email": invite_email},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("proposal_speaker_manage", args=[self.proposal.pk]),
        )
        # Page should contain a message notification of the invitation.
        self.assertContains(response, self.INVITE_SUCCESS_MESSAGE)
        # Page should contain the invited speaker's email address,
        # since they won't have a name.
        self.assertContains(response, invite_email)

        # Speakers can't be invited to the same proposal twice.
        response = self.client.post(
            path=reverse("proposal_speaker_manage", args=[self.proposal.pk]),
            data={"email": invite_email},
            follow=True,
        )
        self.assertContains(response, self.INVITE_DUPLICATE_MESSAGE)
        self.assertNotContains(response, self.INVITE_SUCCESS_MESSAGE)

    def test_inviting_self(self):
        """Verify that you can't invite yourself to a proposal."""
        response = self.client.post(
            path=reverse("proposal_speaker_manage", args=[self.proposal.pk]),
            data={"email": self.user.email},
        )
        # Page should contain a message notification of the invitation.
        self.assertContains(response, self.INVITE_SELF_MESSAGE)
        self.assertNotContains(response, self.INVITE_SUCCESS_MESSAGE)
