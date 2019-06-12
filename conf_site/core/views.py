import csv
import os
from tempfile import mkstemp
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import View


def csrf_failure(request, reason=""):
    """
    Custom view for users who encounter CSRF errors.

    https://docs.djangoproject.com/en/1.9/ref/settings/#csrf-failure-view

    When we upgrade to Django 1.10, this view can be removed.

    """
    response = TemplateResponse(
        request=request, template="403_csrf.html", status=403)
    return response


class CsvView(View):
    """A abstract view that returns a CSV file as a response."""
    http_method_names = ["get"]

    # Create generic names for required filenames.
    # This should be overwritten by inherited views.
    csv_filename = "export.csv"

    def __init__(self, **kwargs):
        super(CsvView, self).__init__(**kwargs)

        self.temp_filename = mkstemp()[1]
        self.temp_file = open(
            file=self.temp_filename, mode="w", encoding="utf-8"
        )

        # Initialize CSV file.
        self.csv_writer = csv.writer(self.temp_file)

    def get(self, *args, **kwargs):
        # Make sure that everything has been saved.
        self.temp_file.flush()
        os.fsync(self.temp_file.fileno())
        self.temp_file.close()
        # Push CSV to user.
        wrapper = FileWrapper(open(self.temp_filename))
        response = HttpResponse(wrapper, content_type="text/csv")
        response["Content-Disposition"] = (
            "attachment; filename=%s" % self.csv_filename)
        # Sending a Content-Length header gives the user better information
        # about the progress of their download.
        response["Content-Length"] = os.path.getsize(self.temp_filename)
        return response
