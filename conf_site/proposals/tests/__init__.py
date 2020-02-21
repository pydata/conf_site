from django.contrib.auth import get_user_model
from django.test import TestCase

from faker import Faker

from conf_site.proposals.tests.factories import ProposalFactory
from symposion.schedule.tests.factories import (
    ConferenceFactory,
    SectionFactory,
)
from symposion.speakers.models import Speaker


class ProposalTestCase(TestCase):
    def setUp(self):
        # Create base conference infrastructure that has to exist in
        # order to create a Proposal.
        self.conference = ConferenceFactory()
        self.section = SectionFactory()
        self.proposal = ProposalFactory()


class ProposalSpeakerTestCase(ProposalTestCase):
    """Abstract test case where user is the proposal's speaker."""

    def setUp(self):
        super().setUp()

        self.faker = Faker()

        USER_EMAIL = self.faker.email()
        USER_PASSWORD = self.faker.password()
        self.user = get_user_model().objects.create_user(
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
