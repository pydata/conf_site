from django import forms

from constance import config

from .models import Proposal, ProposalKeyword


class ModelMultipleTagChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom form field to allow multiple tag selection.

    See https://stackoverflow.com/a/34207440/113527self.

    """
    widget = forms.CheckboxSelectMultiple

    def prepare_value(self, value):
        if hasattr(value, "tag_id"):
            return value.tag_id
        elif (hasattr(value, "__iter__")
                and not isinstance(value, str)
                and not hasattr(value, "_meta")):
            return [self.prepare_value(v) for v in value]
        else:
            return super(ModelMultipleTagChoiceField,
                         self).prepare_value(value)


class ProposalForm(forms.ModelForm):
    required_css_class = "formfield-required"

    official_keywords = ModelMultipleTagChoiceField(
        label=(
            "Please tag this proposal with all relevant tags, "
            "to assist us with proposal review"
        ),
        queryset=ProposalKeyword.objects.filter(official=True).order_by("name"))    # noqa: E501

    class Meta:
        model = Proposal
        fields = [
            "kind",
            "title",
            "audience_level",
            "description",
            "abstract",
            "already_recording",
            "recording_url",
            "specialized_track",
            "official_keywords",
            "other_language",
            "first_time_at_pydata",
            "affiliation",
            "additional_notes",
            "commitment",
            "mentorship",
            "mentoring",
            "company_sponsor_intro",
            "av_equipment_needed",
            "av_needs",
            "stipend",
            "stipend_amount",
            "recording_release",
            "phone_number",
            "slides_url",
            "code_url",
            "review_ready",
        ]
        widgets = {
            "already_recording": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        delete_code_url = kwargs.pop("delete_code_url", True)
        super(ProposalForm, self).__init__(*args, **kwargs)

        self.fields["description"].widget = forms.Textarea(
            attrs={"maxlength": 400}
        )
        # Don't display kind if this proposal does not already exist,
        # since the kind will be overwritten by
        # symposion.proposals.views.proposal_submit_kind.
        if not self.instance.pk:
            del self.fields["kind"]
        # Don't display keyword fields if keyword support is disabled.
        if not config.PROPOSAL_KEYWORDS:
            del self.fields["official_keywords"]
        # Don't display slide and code repo fields if support is disabled.
        if not config.PROPOSAL_URL_FIELDS:
            del self.fields["slides_url"]
            # Posters need this field.
            if delete_code_url:
                del self.fields["code_url"]

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value


class PosterForm(ProposalForm):
    def __init__(self, *args, **kwargs):
        kwargs["delete_code_url"] = False
        super().__init__(*args, **kwargs)

        self.fields["description"].help_text = ""
        self.fields["description"].label = (
            "Describe your poster in 2500 characters or less. "
            "Feel free to provide links to relevant projects, code and images."
        )
        self.fields["description"].widget = forms.Textarea(
            attrs={"maxlength": 2500}
        )

        self.fields["code_url"].help_text = ""
        self.fields["code_url"].label = "Project or Paper URL, if applicable"

    class Meta:
        model = Proposal
        fields = [
            "kind",
            "affiliation",
            "title",
            "description",
            "code_url",
            "official_keywords",
            "experience",
            "commitment",
            "company_sponsor_intro",
            "recording_release",
            "phone_number",
            "slides_url",
            "review_ready",
        ]

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 2500:
            raise forms.ValidationError(
                u"The description must be less than 2500 characters."
            )
        return value


class SprintForm(ProposalForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields.get("official_keywords", False):
            del self.fields["official_keywords"]

        self.fields["title"].label = "Which library do you want to sprint on?"
        self.fields["experience"].label = (
            "Have you run a sprint before, either in-person or virtually?"
        )
        self.fields["description"].help_text = ""
        self.fields["description"].label = (
            "Please describe any materials you have or intend to create "
            "to help attendees set up their development environment, "
            "submit a pull request, etc. Include links where applicable."
        )

    class Meta:
        model = Proposal
        fields = [
            "kind",
            "title",
            "merge_ability",
            "attendance",
            "num_attendees",
            "issue_curation",
            "experience",
            "description",
            "company_sponsor_intro",
            "recording_release",
            "phone_number",
            "code_url",
            "slides_url",
            "review_ready",
        ]
