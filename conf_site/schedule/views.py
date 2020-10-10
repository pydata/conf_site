from django.http import Http404

from symposion.schedule.models import Presentation
from symposion.speakers.models import Speaker

from conf_site.core.views import CsvView, SlugDetailView, SlugRedirectView


class PresentationDetailView(SlugDetailView):
    context_object_name = "presentation"
    model = Presentation
    template_name = "symposion/schedule/presentation_detail.html"
    view_name = "schedule_presentation_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        presentation = self.get_object()
        # Add schedule to context if it exists.
        context["schedule"] = None
        if presentation.slot:
            context["schedule"] = presentation.slot.day.schedule

        return context

    def render_to_response(self, context, **response_kwargs):
        presentation = self.get_object()

        # Do not render if presentation is cancelled.
        if presentation.cancelled:
            raise Http404()

        # Verify that schedule is published (or user is staff).
        if presentation.slot is not None:
            schedule = presentation.slot.day.schedule
            if not schedule.published and not self.request.user.is_staff:
                raise Http404()

        return super().render_to_response(context, **response_kwargs)


class PresentationRedirectView(SlugRedirectView):
    model = Presentation
    redirect_view_name = "schedule_presentation_detail"


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
                if not presentation.cancelled:
                    self.csv_writer.writerow(
                        [
                            speaker.name,
                            speaker.email,
                            presentation.title,
                            presentation.proposal.kind.name,
                        ]
                    )

        return super(ExportPresentationSpeakerView, self).get(*args, **kwargs)
