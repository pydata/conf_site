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
