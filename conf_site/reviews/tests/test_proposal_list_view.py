# -*- coding: utf-8 -*-
from random import randint

from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from faker import Faker

from symposion.proposals.models import AdditionalSpeaker
from symposion.schedule.tests.factories import (
    ProposalKindFactory, SectionFactory
)

from conf_site.accounts.tests import AccountsTestCase
from conf_site.proposals.models import Proposal
from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.reviews.models import ProposalResult
from conf_site.reviews.tests import ReviewingTestCase
from conf_site.speakers.tests.factories import SpeakerFactory


class ProposalListViewTestCase(ReviewingTestCase, AccountsTestCase):
    reverse_view_name = "review_proposal_list"

    def setUp(self):
        super(ProposalListViewTestCase, self).setUp()
        self.faker = Faker()

    def _validate_proposals(self, proposals, should_contain=True):
        # User must be in the reviewers group in order to access
        # this view.
        self._add_to_reviewers_group()
        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        for proposal in proposals:
            if should_contain:
                self.assertContains(response, proposal.title)
            else:
                self.assertNotContains(response, proposal.title)

    def test_no_cancelled_proposals(self):
        """Verify that cancelled proposals do not appear in proposal list."""
        VALID_PROPOSAL_COUNT = 4
        INVALID_PROPOSAL_COUNT = 3

        # Create proposals.
        valid_proposals = ProposalFactory.create_batch(
            size=VALID_PROPOSAL_COUNT, cancelled=False
        )
        invalid_proposals = ProposalFactory.create_batch(
            size=INVALID_PROPOSAL_COUNT, cancelled=True
        )

        self._validate_proposals(valid_proposals, True)
        self._validate_proposals(invalid_proposals, False)

    def test_proposal_count(self):
        """Verify that proposal list contains count of proposals."""
        self._add_to_reviewers_group()
        # Setup the ProposalKinds for talks and tutorials.
        section = SectionFactory()
        talk_kind = ProposalKindFactory.create(
            section=section, name="Talk", slug="talk"
        )
        tutorial_kind = ProposalKindFactory.create(
            section=section, name="Tutorial", slug="tutorial"
        )
        # Create a random number of talks and tutorials.
        num_talks = randint(2, 10)
        num_tutorials = randint(2, 10)
        num_total_proposals = num_talks + num_tutorials
        ProposalFactory.create_batch(size=num_talks, kind=talk_kind)
        ProposalFactory.create_batch(size=num_tutorials, kind=tutorial_kind)

        response = self.client.get(
            reverse(self.reverse_view_name, args=self.reverse_view_args)
        )
        self.assertContains(
            response,
            "<strong>{}</strong> proposals".format(num_total_proposals),
        )
        self.assertContains(
            response, "<strong>{}</strong> talks".format(num_talks)
        )
        self.assertContains(
            response, "<strong>{}</strong> tutorials".format(num_tutorials)
        )

    def test_changing_proposal_status(self):
        self._become_superuser()
        # Create multiple proposals.
        proposals = ProposalFactory.create_batch(size=randint(3, 6))
        for result_status in ProposalResult.RESULT_STATUSES:
            # Use post data to change the first two proposals' statuses.
            post_data = {
                "proposal_pk": [proposals[0].pk, proposals[1].pk],
                "mark_status": result_status[0],
            }
            response = self.client.post(reverse("review_multiedit"), post_data)
            # Verify that we are redirected to the correct page
            # (a list of proposals with the same changed status).
            self.assertRedirects(
                response,
                reverse(
                    "review_proposal_result_list", args=[result_status[0]]
                ),
            )
            # Verify that the first two proposals' status has changed
            #  and all other proposals have remained the same.
            for proposal in Proposal.objects.all():
                if proposal.pk in post_data["proposal_pk"]:
                    self.assertEqual(
                        proposal.review_result.status, result_status[0]
                    )
                else:
                    self.assertEqual(
                        proposal.review_result.status,
                        ProposalResult.RESULT_UNDECIDED,
                    )

    def test_creating_presentations(self):
        self._become_superuser()
        proposals = ProposalFactory.create_batch(size=3)
        # Create a single presentation and validate the response.
        post_data = {
            "proposal_pk": [proposals[0].pk],
            "create_presentations": "show me a presentation",
        }
        response = self.client.post(
            reverse("review_multiedit"), post_data, follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                "review_proposal_result_list",
                args=[ProposalResult.RESULT_ACCEPTED],
            ),
        )
        self.assertContains(response, "1 presentation created")

        # Verify that POSTing the same data does not create an
        # additional presentation.
        response = self.client.post(
            reverse("review_multiedit"), post_data, follow=True
        )
        self.assertContains(
            response, "All selected proposals already had presentations"
        )

        # Verify that the other two proposals do not have presentations.
        for proposal in Proposal.objects.all():
            if proposal.pk == post_data["proposal_pk"][0]:
                # Verify that the first proposal has a presentation
                # and that their metadata is the same.
                self.assertEqual(proposal.title, proposal.presentation.title)
            else:
                with self.assertRaises(ObjectDoesNotExist):
                    proposal.presentation

        # Verify that creating multiple presentations works.
        post_data["proposal_pk"] = [proposals[1].pk, proposals[2].pk]
        response = self.client.post(
            reverse("review_multiedit"), post_data, follow=True
        )
        self.assertContains(response, "2 presentations created")
        # All proposals should now have presentations.
        for proposal in Proposal.objects.all():
            self.assertEqual(proposal.title, proposal.presentation.title)

    def test_sending_notifications(self):
        self._become_superuser()
        notified_proposal = ProposalFactory()
        # Create additional proposals.
        ProposalFactory.create_batch(size=2)

        from_address = self.faker.email()
        subject = self.faker.sentence()
        body = self.faker.paragraph()

        post_data = {
            "body": body,
            "from_address": from_address,
            "proposal_pk": notified_proposal.pk,
            "send_notification": True,
            "subject": subject,
        }
        response = self.client.post(
            reverse("review_multiedit"), post_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    def test_warning_about_unnotified_speakers(self):
        self._become_superuser()
        proposal = ProposalFactory()
        emailless_speaker = SpeakerFactory(user=None)
        # Add an additional **confirmed** speaker that
        # does not have an email address.
        proposal.additional_speakers.add(emailless_speaker)
        additional_speaker = AdditionalSpeaker.objects.get(
            speaker=emailless_speaker, proposalbase=proposal
        )
        additional_speaker.status = AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED
        additional_speaker.save()

        post_data = {
            "body": self.faker.paragraph(),
            "from_address": self.faker.email(),
            "proposal_pk": proposal.pk,
            "send_notification": True,
            "subject": self.faker.sentence(),
        }
        response = self.client.post(
            reverse("review_multiedit"), post_data, follow=True
        )
        speaker_warning = (
            "Speaker {} does not have an email address "
            "and has not been notified.".format(emailless_speaker.name)
        )
        self.assertContains(response, speaker_warning)
