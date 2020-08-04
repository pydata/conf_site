from constance import config

from conf_site.core.views import CsvView
from conf_site.proposals.models import Proposal
from conf_site.reviews.models import ProposalResult


class ExportProposalSubmittersView(CsvView):
    """Export information about proposal submitters."""

    csv_filename = "proposal-submitters.csv"
    header_row = [
        "Submitter Name",
        "Submitter Email",
        "Proposal Name",
        "Proposal Type",
    ]

    def _write_submitter_row(self, submitter, proposal):
        """Utility method to write a row for an individual submitter."""
        self.csv_writer.writerow(
            [
                submitter.name,
                submitter.email,
                proposal.title,
                proposal.kind.name,
            ]
        )

    def get(self, *args, **kwargs):
        for proposal in Proposal.objects.order_by("title"):
            self._write_submitter_row(proposal.speaker, proposal)
            for additional_submitter in proposal.additional_speakers.all():
                self._write_submitter_row(additional_submitter, proposal)

        return super(ExportProposalSubmittersView, self).get(*args, **kwargs)


class ExportProposalsView(CsvView):
    """Export information about submitted proposals."""

    csv_filename = "proposals.csv"
    header_row = [
        "Number",
        "Title",
        "Primary Speaker Name",
        "Primary Speaker Email",
        "All Speaker Email Addresses",
        "Kind",
        "Audience Level",
        "Keywords",
        "Slides",
        "Repository",
        "First Time at PyData",
        "Affiliation",
        "Sponsoring",
        "Phone Number",
        "Status",
        "Date Created",
        "Date Modified",
    ]

    def get(self, *args, **kwargs):
        # Iterate through proposals.
        for proposal in Proposal.objects.order_by("pk"):
            accepted_speaker_email_addresses = ", ".join(
                speaker.email for speaker in proposal.speakers()
            )
            if proposal.cancelled:
                proposal_status = "Cancelled"
            else:
                try:
                    proposal_status = (
                        proposal.review_result.get_status_display()
                    )
                except ProposalResult.DoesNotExist:
                    proposal_status = dict(ProposalResult.RESULT_STATUSES).get(
                        ProposalResult.RESULT_UNDECIDED
                    )
            if config.PROPOSAL_KEYWORDS:
                keywords = ", ".join(
                    map(
                        lambda keyword: keyword.name,
                        proposal.official_keywords.all(),
                    )
                )
            else:
                keywords = ""
            self.csv_writer.writerow(
                [
                    proposal.number,
                    proposal.title,
                    proposal.speaker.name,
                    proposal.speaker.email,
                    accepted_speaker_email_addresses,
                    proposal.kind.name,
                    proposal.get_audience_level_display(),
                    keywords,
                    proposal.slides_url,
                    proposal.code_url,
                    proposal.get_first_time_at_pydata_display(),
                    proposal.affiliation,
                    proposal.get_sponsoring_interest_display(),
                    proposal.phone_number,
                    proposal_status,
                    proposal.date_created,
                    proposal.date_last_modified,
                ]
            )

        return super().get(*args, **kwargs)
