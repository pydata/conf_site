from django import forms

from constance import config
from markitup.widgets import MarkItUpWidget

from .models import Proposal, ProposalKeyword


class ProposalForm(forms.ModelForm):
    official_keywords = forms.ModelMultipleChoiceField(
        label="Official Keywords",
        queryset=ProposalKeyword.objects.filter(official=True).order_by("name"),     # noqa: E501
        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Proposal
        fields = [
            "title",
            "audience_level",
            "description",
            "abstract",
            "first_time_at_pydata",
            "affiliation",
            "under_represented_population",
            "under_represented_details",
            "under_represented_other",
            "additional_notes",
            "recording_release",
            "phone_number",
            "slides_url",
            "code_url",
            "official_keywords",
            "user_keywords",
        ]
        widgets = {
            "abstract": MarkItUpWidget(),
            "additional_notes": MarkItUpWidget(),
            "under_represented_details": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)

        # Don't display keyword fields if keyword support is disabled.
        if not config.PROPOSAL_KEYWORDS:
            del self.fields["official_keywords"]
            del self.fields["user_keywords"]
        # Don't display slide and code repo fields if support is disabled.
        if not config.PROPOSAL_URL_FIELDS:
            del self.fields["slides_url"]
            del self.fields["code_url"]

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value
