from django.contrib.auth import get_user_model
from django.test import TestCase

from symposion.conference.models import Conference, Section
from symposion.proposals.models import ProposalBase
from symposion.speakers.models import Speaker
from symposion.schedule.models import Presentation
from symposion.schedule.tests.factories import ProposalKindFactory


class UserlessSpeakersTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two speakers - one with a User attached, and one without.
        user_model = get_user_model()
        user = user_model.objects.create(
            username="test",
            email="example@example.com",
            first_name="Test",
            last_name="User",
        )
        primary_speaker = Speaker.objects.create(user=user, name="Speaker #1")
        cls.second_speaker = Speaker.objects.create(
            user=None, name="Speaker #2"
        )

        # A Presentation needs a ProposalBase, and
        # a ProposalBase needs a ProposalKind, and
        # a ProposalKind needs a Section, and
        # A Section needs a Conference, and
        # the developer who wrote this test case needs a hug!
        conference = Conference.objects.create(title="Conference")
        section = Section.objects.create(
            conference=conference, name="Section", slug="section"
        )
        proposal_kind = ProposalKindFactory.create(section=section)
        proposal_base = ProposalBase.objects.create(
            title="Proposal",
            description="...",
            abstract="...",
            speaker=primary_speaker,
            kind=proposal_kind,
        )
        cls.presentation = Presentation.objects.create(
            title="Presentation",
            description="...",
            abstract="...",
            speaker=primary_speaker,
            proposal_base=proposal_base,
            section=section,
        )
        cls.presentation.additional_speakers.add(cls.second_speaker)

    def test_userless_speaker_name(self):
        """Test that userless speakers will display their names."""
        self.assertEqual(str(self.second_speaker), self.second_speaker.name)

    def test_presentation_userless_speakers(self):
        """Test that presentation speaker counts include all speakers."""
        # A Presentation's speakers() method is a generator of all
        # associated speakers who have accepted their association.
        # If it is properly returning all accepted speakers,
        # the result should be one (not two).
        self.assertEqual(len(list(self.presentation.speakers())), 1)
