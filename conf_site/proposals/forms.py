from django import forms

from constance import config

from .models import Proposal, ProposalKeyword, ProposalTrack


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

    YES_NO_CHOICES = ((True, "Yes"), (False, "No"))
    recording_online = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        initial=False,
        label="Is there a recording of this talk/tutorial already online?",
        required=True,
    )

    tracks = ModelMultipleTagChoiceField(
        label=(
            "Please choose one or more specialized tracks, "
            "if any, your proposal would fit into"
        ),
        required=False,
        queryset=ProposalTrack.objects.all(),
    )
    official_keywords = ModelMultipleTagChoiceField(
        label="Keywords",
        queryset=ProposalKeyword.objects.filter(official=True).order_by("name"))    # noqa: E501

    class Meta:
        model = Proposal
        fields = [
            "kind",
            "title",
            "prior_knowledge",
            "prior_knowledge_details",
            "description",
            "outline",
            "abstract",
            "recording_online",
            "recording_url",
            "tracks",
            "official_keywords",
            "country",
            "affiliation",
            "additional_notes",
            "accessibility_needs",
            "first_time_at_pydata",
            "under_represented_group",
            "under_represented_details",
            "under_represented_other",
            "sponsoring_interest",
            "recording_release",
            "phone_number",
            "slides_url",
            "code_url",
        ]
        widgets = {
            "under_represented_details": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)

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
            del self.fields["code_url"]

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value
