from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string

from symposion.speakers.models import Speaker

from conf_site.proposals.tests import ProposalTestCase


class ProposalSpeakerManageViewTestCase(ProposalTestCase):
    """Automated test cases for symposion's proposal_speaker_manage view."""

    def setUp(self):
        super(ProposalSpeakerManageViewTestCase, self).setUp()
        user_model = get_user_model()
        USER_EMAIL = "example@example.com"
        USER_PASSWORD = get_random_string()
        self.user = user_model.objects.create_user(
            username="user", email=USER_EMAIL, password=USER_PASSWORD
        )
        speaker = Speaker.objects.create(name="Nancy Pelosi")
        speaker.user = self.user
        speaker.save()

        # Overwrite speaker for this case's proposal - sorry, Paul Ryan.
        self.proposal.speaker = speaker
        self.proposal.save()

        self.assertTrue(
            self.client.login(username=USER_EMAIL, password=USER_PASSWORD)
        )

    def test_verify_proposal_jacking_does_not_work(self):
        """Verify that you can't manage a proposal that is not yours."""
        # Create a new speaker and change ownership of this
        # test case's Proposal to said speaker.
        other_speaker = Speaker.objects.create(name="Other Speaker")
        self.proposal.speaker = other_speaker
        self.proposal.save()

        response = self.client.get(
            reverse("proposal_speaker_manage", args=[self.proposal.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_inviting_speaker(self):
        """Verify that inviting a speaker works."""
        response = self.client.post(
            path=reverse("proposal_speaker_manage", args=[self.proposal.pk]),
            data={"email": "valid@example.com"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("proposal_speaker_manage", args=[self.proposal.pk]),
        )
        self.assertContains(response, "Speaker invited to proposal.")
