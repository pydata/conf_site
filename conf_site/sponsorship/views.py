from symposion.sponsorship.models import Sponsor

from conf_site.core.views import CsvView


class ExportSponsorsView(CsvView):
    """Export information about active sponsors to CSV file."""

    csv_filename = "sponsors.csv"
    header_row = ["Name", "URL", "Contact Name", "Contact Email", "Level"]

    def get(self, *args, **kwargs):
        # Add all **active** sponsors to CSV file.
        for sponsor in Sponsor.objects.filter(active=True):
            self.csv_writer.writerow(
                [
                    sponsor.name,
                    sponsor.external_url,
                    sponsor.contact_name,
                    sponsor.contact_email,
                    sponsor.level,
                ]
            )

        return super(ExportSponsorsView, self).get(*args, **kwargs)
