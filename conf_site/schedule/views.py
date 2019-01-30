from symposion.speakers.models import Speaker

from conf_site.core.views import CsvView


class ExportPresentationSpeakerView(CsvView):
    """Export information about speakers and presentations."""

    csv_filename = "speakers-with-presentation-emails.csv"

    def get(self, *args, **kwargs):
        self.csv_writer.writerow(
            [
                "Speaker Name",
                "Speaker Email",
                "Presentation Name",
                "Presentation Type",
            ]
        )

        # Iterate through speakers and presentations.
        for speaker in Speaker.objects.all():
            for presentation in speaker.all_presentations:
                self.csv_writer.writerow(
                    [
                        speaker.name,
                        speaker.email,
                        presentation.title,
                        presentation.proposal.kind.name,
                    ]
                )

        return super(ExportPresentationSpeakerView, self).get(*args, **kwargs)
