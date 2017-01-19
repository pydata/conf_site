from django import forms

from markitup.widgets import MarkItUpWidget

from .models import Proposal


class ProposalForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = [
            "title",
            "audience_level",
            "description",
            "abstract",
            "under_represented_population",
            "under_represented_details",
            "additional_notes",
            "recording_release",
        ]
        widgets = {
            "abstract": MarkItUpWidget(),
            "additional_notes": MarkItUpWidget(),
            "under_represented_details": forms.CheckboxSelectMultiple(),
        }

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value
