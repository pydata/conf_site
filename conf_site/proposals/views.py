from conf_site.core.views import CsvView
from conf_site.proposals.models import Proposal


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
        "Gender",
        "Group Identity",
        "Date Created",
        "Date Modified",
    ]

    def get(self, *args, **kwargs):
        # Iterate through proposals.
        for proposal in Proposal.objects.order_by("pk"):
            accepted_speaker_email_addresses = ", ".join(
                speaker.email for speaker in proposal.speakers()
            )
            self.csv_writer.writerow(
                [
                    proposal.number,
                    proposal.title,
                    proposal.speaker.name,
                    proposal.speaker.email,
                    accepted_speaker_email_addresses,
                    proposal.kind.name,
                    proposal.get_audience_level_display(),
                    proposal.gender,
                    proposal.get_under_represented_group_display(),
                    proposal.date_created,
                    proposal.date_last_modified,
                ]
            )

        return super().get(*args, **kwargs)
