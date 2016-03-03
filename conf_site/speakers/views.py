import os
from tempfile import mkstemp

import unicodecsv

from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.views.generic import View

from symposion.speakers.models import Speaker


class ExportAcceptedSpeakerEmailView(View):
    """Export email addresses of speakers with accepted presentations."""
    http_method_names = ["get"]

    def get(self, *args, **kwargs):
        CSV_ENCODING = "utf-8"
        CSV_FILENAME = "accepted-speakers.csv"
        CSV_MIMETYPE = "text/csv"

        # Create temporary file.
        # mkstemp's first parameter is a file descriptor that we don't need.
        temp_filename = mkstemp()[1]
        temp_file = open(temp_filename, "w")
        # Initialize CSV file.
        csv_writer = unicodecsv.writer(temp_file, encoding=CSV_ENCODING)
        csv_writer.writerow(["Name", "Email Address"])

        # Iterate through speakers.
        # Add speakers with accepted presentations to temp file.
        for speaker in Speaker.objects.all():
            if speaker.all_presentations:
                csv_writer.writerow([speaker.name, speaker.email])

        # Make sure that everything has been saved.
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()

        # Push CSV to user.
        wrapper = FileWrapper(open(temp_filename))
        response = HttpResponse(wrapper, content_type=CSV_MIMETYPE)
        response["Content-Disposition"] = (
            "attachment; filename=%s" % CSV_FILENAME)
        # Sending a Content-Length header gives the user better information
        # about the progress of their download.
        response["Content-Length"] = os.path.getsize(temp_filename)
        return response
