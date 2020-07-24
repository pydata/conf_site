from django.contrib import messages
from django.template.defaultfilters import pluralize
from django.urls import reverse_lazy

from conf_site.core.views import CsvImportView, SuperuserOnlyView
from conf_site.reviews.tasks import import_reviewer_csv


class ReviewerCsvImportView(SuperuserOnlyView, CsvImportView):
    success_url = reverse_lazy("reviewer_import")
    template_name = "reviews/reviewer_import.html"

    def process(self, filename, user_id):
        result = import_reviewer_csv(filename)
        if result:
            messages.success(
                self.request,
                "{} user{} created. {} existing user{} found.".format(
                    result[0],
                    pluralize(result[0]),
                    result[1],
                    pluralize(result[1]),
                ),
            )
        else:
            messages.error(
                self.request, "Unable to successfully import CSV file."
            )
