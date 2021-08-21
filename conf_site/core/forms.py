from django import forms


class CsvUploadForm(forms.Form):
    """Form for uploading a CSV file."""

    csv_file = forms.FileField(label="Please upload a CSV file.")

    def _is_csv_file(self, file_data):
        """
        Test whether an uploaded file is a CSV file.

        Returns a list of a boolean of the results and the uploaded content
        type.
        """
        uploaded_content_type = getattr(file_data, "content_type", "text/csv")
        return [uploaded_content_type == "text/csv", uploaded_content_type]

    def clean_csv_file(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        results = self._is_csv_file(data["csv_file"])
        if not results[0]:
            raise forms.ValidationError(
                "Only CSV files ('text/csv') can be uploaded with this form. "
                "You uploaded a '{}' file.".format(results[1])
            )
        return data
