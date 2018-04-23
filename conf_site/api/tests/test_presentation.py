from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import status
from symposion.conference.models import Section
from symposion.schedule.models import (
    Presentation,
    Slot,
    SlotKind,
    Schedule,
    Day,
)
from symposion.proposals.models import ProposalKind
from symposion.speakers.models import Speaker, User

from conf_site.api.tests import ConferenceSiteAPITestCase
from conf_site.proposals.models import Proposal


class ConferenceSiteAPISponsorTestCase(ConferenceSiteAPITestCase):

    @classmethod
    def setUpTestData(cls):
        super(ConferenceSiteAPISponsorTestCase, cls).setUpTestData()
        cls.speaker = Speaker.objects.create(
            user=User.objects.create_user('test', 'test@pydata.org', 'test'),
            name='test speaker',
        )
        section = Section.objects.create(
            name="FooBarSection",
            slug="foo-bar",
            conference=cls.conference,
        )
        cls.schedule = Schedule.objects.create(section=section)
        proposal_kind = ProposalKind.objects.create(
            section=section,
            name="Kind of Proposal",
            slug="proposal-kind",
        )
        cls.presentation = Presentation.objects.create(
            slot=Slot.objects.create(
                name='test slot',
                day=Day.objects.create(
                    schedule=cls.schedule,
                    date=timezone.now().date(),
                ),
                kind=SlotKind.objects.create(
                    schedule=cls.schedule,
                    label='45-min talk',
                ),
                start=timezone.now(),
                end=timezone.now(),
            ),
            title='test presentation',
            description='test description',
            abstract='test abstract',
            speaker=cls.speaker,
            proposal_base=Proposal.objects.create(
                kind=proposal_kind,
                title='Test proposal',
                description='lorem ipsum'*15,
                abstract='lorem ipsum'*15,
                speaker=cls.speaker,
                audience_level=Proposal.AUDIENCE_LEVEL_NOVICE,
            ),
            section=Section.objects.first(),
        )

    def test_presentation_list_api_anonymous_user(self):
        response = self.client.get(reverse('presentation-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_presentation_list_api_admin_user(self):
        self.client.login(username='admin@pydata.org', password='admin')
        response = self.client.get(reverse('presentation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_presentation_detail_api_anonymous_user(self):
        response = self.client.get(
            reverse('presentation-detail', args=[self.presentation.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_presentation_detail_api_admin_user(self):
        self.client.login(username='admin@pydata.org', password='admin')
        response = self.client.get(
            reverse('presentation-detail', args=[self.presentation.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
