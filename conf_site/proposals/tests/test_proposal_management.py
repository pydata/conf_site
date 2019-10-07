from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.crypto import get_random_string

from faker import Faker

from conf_site.proposals.tests import ProposalTestCase
from symposion.speakers.models import Speaker


class ProposalSpeakerManageViewTestCase(ProposalTestCase):
    """Automated test cases for symposion's proposal_speaker_manage view."""

    def setUp(self):
        super(ProposalSpeakerManageViewTestCase, self).setUp()

        self.faker = Faker()

        user_model = get_user_model()
        USER_EMAIL = self.faker.email()
        USER_PASSWORD = get_random_string()
        self.user = user_model.objects.create_user(
            username=self.faker.profile()["username"],
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )
        speaker = Speaker.objects.create(name=self.faker.name())
        speaker.user = self.user
        speaker.save()

        # Overwrite speaker for this case's proposal.
        self.proposal.speaker = speaker
        self.proposal.save()

        self.assertTrue(
            self.client.login(username=USER_EMAIL, password=USER_PASSWORD)
        )

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
        """Verify that inviting a speaker works."""
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
        self.assertContains(response, "Speaker invited to proposal.")
        # Page should contain the invited speaker's email address,
        # since they won't have a name.
        self.assertContains(response, invite_email)
