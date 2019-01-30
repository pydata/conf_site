from django.db.models import Q
from django.views.generic import ListView

from symposion.speakers.models import Speaker

from conf_site.core.views import CsvView


class SpeakerListView(ListView):
    """Show all speakers with presentations."""

    context_object_name = "speakers"
    queryset = (
        Speaker.objects.filter(
            Q(presentations__gt=0) | Q(copresentations__gt=0)
        )
        .order_by()
        .distinct()
    )
    template_name = "speakers/speaker_list.html"


class ExportAcceptedSpeakerEmailView(CsvView):
    """Export email addresses of speakers with accepted presentations."""
    csv_filename = "accepted-speaker-emails.csv"

    def get(self, *args, **kwargs):
        self.csv_writer.writerow(["Name", "Email Address"])

        # Iterate through speakers.
        # Add speakers with accepted presentations to temp file.
        for speaker in Speaker.objects.all():
            if speaker.all_presentations:
                self.csv_writer.writerow([speaker.name, speaker.email])

        return super(ExportAcceptedSpeakerEmailView, self).get(*args, **kwargs)
