from django import forms


class CsvUploadForm(forms.Form):
    """Form for uploading a CSV file."""

    csv_file = forms.FileField(label="Please upload a CSV file.")
