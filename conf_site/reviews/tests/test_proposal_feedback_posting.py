from django.core import mail

from conf_site.accounts.tests import AccountsTestCase
from conf_site.accounts.tests.factories import UserFactory
from conf_site.reviews.tests import ReviewingPostViewTestCase
from conf_site.reviews.tests.factories import ProposalFeedbackFactory


class ProposalFeedbackPostingTestCase(
    ReviewingPostViewTestCase, AccountsTestCase
):
    reverse_view_name = "review_proposal_feedback"

    def setUp(self):
        super().setUp()

        self.reverse_view_data = {
            "comment": self.faker.paragraph(
                nb_sentences=5, variable_nb_sentences=True
            )
        }

    def _duplicate_email_addresses(self, message):
        """
        Helper method to find if an email message contains duplicate addresses.
        """
        seen_addresses = []

        def _search_for_duplicates(email_field):
            for address in email_field:
                if address in seen_addresses:
                    return True
                else:
                    seen_addresses.append(address)

        _search_for_duplicates(message.to)
        _search_for_duplicates(message.cc)
        _search_for_duplicates(message.bcc)
        return False

    def test_no_duplicate_speaker_emails_when_sending_feedback(self):
        self._add_to_reviewers_group()
        # Create multiple existing proposal feedback authored by the speaker.
        ProposalFeedbackFactory.create_batch(
            proposal=self.proposal, author=self.proposal.speaker.user, size=3
        )

        response = self._get_response()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)
        for message in mail.outbox:
            self.assertFalse(self._duplicate_email_addresses(message))

    def test_no_duplicate_reviewer_emails_when_sending_feedback(self):
        self._i_am_the_speaker_now()
        # Create multiple existing proposal feedback authored by a random user.
        random_user = UserFactory()
        ProposalFeedbackFactory.create_batch(
            proposal=self.proposal, author=random_user, size=3
        )

        response = self._get_response()

        self.assertEqual(response.status_code, 200)
        # There should be only one message sent - to the random user.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [random_user.email])
        self.assertFalse(self._duplicate_email_addresses(mail.outbox[0]))
