from django.contrib.auth.models import Group

from conf_site.core.views import CsvView


class ExportReviewersView(CsvView):
    csv_filename = "reviewers.csv"
    header_row = ["ID", "Name", "Email"]

    def get(self, *args, **kwargs):
        reviewers_group = Group.objects.get(name="Reviewers")
        for reviewer in reviewers_group.user_set.all():
            self.csv_writer.writerow(
                [
                    reviewer.id,
                    reviewer.get_full_name(),
                    reviewer.email,
                ]
            )

        return super().get(*args, **kwargs)
