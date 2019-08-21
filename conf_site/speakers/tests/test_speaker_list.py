from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from conf_site.accounts.tests import AccountsTestCase
from conf_site.schedule.tests.factories import PresentationFactory
from conf_site.speakers.tests.factories import SpeakerFactory
from symposion.conference.models import Conference, Section
from symposion.proposals.models import ProposalBase, ProposalKind
from symposion.schedule.models import (
    Presentation,
    Slot,
    SlotKind,
    Schedule,
    Day,
)
from symposion.speakers.models import Speaker


class SpeakerListViewTestCase(AccountsTestCase):
    """Verify that a presentation's primary & secondary speakers are shown."""

    def setUp(self):
        super(SpeakerListViewTestCase, self).setUp()

        conference = Conference.objects.create(title="Conference")
        self.section = Section.objects.create(
            conference=conference, name="Section", slug="section"
        )
        schedule = Schedule.objects.create(section=self.section)
        self.day = Day.objects.create(
            schedule=schedule, date=timezone.now().date()
        )
        self.slot_kind = SlotKind.objects.create(
            schedule=schedule, label="slot kind"
        )
        self.proposal_kind = ProposalKind.objects.create(
            section=self.section, name="Kind", slug="kind"
        )

    def _unpublish_schedule(self):
        """Utility method to unpublish associated schedule."""
        schedule = self.section.schedule
        schedule.published = False
        schedule.save()

    def test_speaker_list_unviewable_when_schedule_is_unpublished(self):
        """Verify that if schedule is unpublished, page does not appear."""
        self._unpublish_schedule()
        response = self.client.get(reverse("speaker_list"))
        # Regular users should get redirected to the login page,
        # because SpeakerListView.raise_exception is False.
        login_url_redirecting_to_speaker_list = "{}?next={}".format(
            settings.LOGIN_URL, reverse("speaker_list")
        )
        self.assertEqual(response.url, login_url_redirecting_to_speaker_list)

    def test_staff_access_to_speaker_list_with_unpublished_schedule(self):
        """
        Verify that staff can access list when schedule is unpublished.
        """
        self._unpublish_schedule()
        self._become_staff()
        self.client.login(username=self.user.email, password=self.password)
        response = self.client.get(reverse("speaker_list"))
        self.assertEqual(response.status_code, 200)

    def test_superuser_access_to_speaker_list_with_unpublished_schedule(self):
        """
        Verify that superusers can access list when schedule is unpublished.
        """
        self._unpublish_schedule()
        self._become_superuser()
        self.client.login(username=self.user.email, password=self.password)
        response = self.client.get(reverse("speaker_list"))
        self.assertEqual(response.status_code, 200)

    def test_unaccepted_speakers(self):
        """Verify that speakers without presentations do not appear."""
        speaker = Speaker.objects.create(name="No Accepted Presentations")
        self.assertEqual(speaker.presentations.count(), 0)
        response = self.client.get(reverse("speaker_list"))
        self.assertNotContains(response, speaker.name)

    def test_no_duplicate_speakers(self):
        """Verify that a speaker is only shown once."""
        # Create a speaker with two accepted presentations.
        speaker = Speaker.objects.create(name="Two Accepted Presentations")
        Presentation.objects.create(
            slot=Slot.objects.create(
                day=self.day,
                kind=self.slot_kind,
                start=timezone.now(),
                end=timezone.now(),
            ),
            title="#1",
            description="Description",
            abstract="Abstract",
            speaker=speaker,
            proposal_base=ProposalBase.objects.create(
                title="#1",
                description="Description",
                abstract="Abstract",
                kind=self.proposal_kind,
                speaker=speaker,
            ),
            section=self.section,
        )
        Presentation.objects.create(
            slot=Slot.objects.create(
                day=self.day,
                kind=self.slot_kind,
                start=timezone.now(),
                end=timezone.now(),
            ),
            title="#2",
            description="Description",
            abstract="Abstract",
            speaker=speaker,
            proposal_base=ProposalBase.objects.create(
                title="#2",
                description="Description",
                abstract="Abstract",
                kind=self.proposal_kind,
                speaker=speaker,
            ),
            section=self.section,
        )
        self.assertEqual(speaker.presentations.count(), 2)
        response = self.client.get(reverse("speaker_list"))
        self.assertContains(response=response, text=speaker.name, count=1)

    def test_one_presentation_two_speakers(self):
        """Verify that secondary speakers appear in the speaker list."""
        speaker1 = Speaker.objects.create(name="Speaker Number One")
        speaker2 = Speaker.objects.create(name="Speaker Number Two")
        presentation = Presentation.objects.create(
            slot=Slot.objects.create(
                day=self.day,
                kind=self.slot_kind,
                start=timezone.now(),
                end=timezone.now(),
            ),
            title="#1",
            description="Description",
            abstract="Abstract",
            speaker=speaker1,
            proposal_base=ProposalBase.objects.create(
                title="#1",
                description="Description",
                abstract="Abstract",
                kind=self.proposal_kind,
                speaker=speaker1,
            ),
            section=self.section,
        )
        presentation.additional_speakers.add(speaker2)
        response = self.client.get(reverse("speaker_list"))
        self.assertContains(response=response, text=speaker1.name, count=1)
        self.assertContains(response=response, text=speaker2.name, count=1)

    def test_omitting_nameless_speakers(self):
        """Verify that speakers without a name do not appear."""
        presentation = PresentationFactory()
        speaker2 = SpeakerFactory()
        # Ensure that this speaker doesn't have a name.
        speaker2.name = ""
        speaker2.save()
        presentation.additional_speakers.add(speaker2)
        response = self.client.get(reverse("speaker_list"))
        # Since speaker2 is nameless, we check for a link to their
        # speaker page in the response instead of their
        # non-existent name.
        speaker2_url = reverse(
            "speaker_profile", args=[speaker2.pk, speaker2.slug]
        )
        self.assertNotContains(response, speaker2_url)
