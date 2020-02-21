from django.urls import reverse

from constance.test import override_config

from conf_site.proposals.tests import ProposalSpeakerTestCase
from symposion.proposals.models import ProposalSection


class ProposalEditingViewTestCase(ProposalSpeakerTestCase):
    def setUp(self):
        super().setUp()

        # Retrieve ProposalSection.
        # We use `get_or_create` here because the ProposalSection
        # isn't automatically created.
        self.proposal_section = ProposalSection.objects.get_or_create(
            section=self.proposal.section
        )[0]

    def _proposal_edit_response(self):
        """Helper method to get response from `proposal_edit` view."""
        proposal_kind_slug = self.proposal.kind.slug
        proposal_forms = {
            proposal_kind_slug: "conf_site.proposals.forms.ProposalForm"
        }
        with self.settings(PROPOSAL_FORMS=proposal_forms):
            return self.client.get(
                reverse("proposal_edit", args=[self.proposal.pk])
            )

    @override_config(PROPOSAL_EDITING_WHEN_CFP_IS_CLOSED=True)
    def test_ability_to_edit_if_setting_is_disabled(self):
        """Verify whether SETTING = False ignores restrictions."""
        response = self._proposal_edit_response()
        self.assertTemplateUsed(
            response, "symposion/proposals/proposal_edit.html"
        )

    @override_config(PROPOSAL_EDITING_WHEN_CFP_IS_CLOSED=False)
    def test_inability_to_edit_when_section_is_closed(self):
        """Verify whether closing the section can disable editing proposals."""

        self.proposal_section.closed = True
        self.proposal_section.save()
        self.assertFalse(self.proposal_section.is_available())

        response = self._proposal_edit_response()
        self.assertTemplateUsed(
            response, "symposion/proposals/proposal_error.html"
        )
