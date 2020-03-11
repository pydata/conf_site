from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout

from conf_site.proposals.models import Proposal


SECTION1_LEGEND = (
    "<h4>The following information will be listed publicly "
    "in the conference program for a {{ kind.name|lower }}. "
    "This information should include what the {{ kind.name|lower }} "
    "is about and why it is interesting, the target audience for "
    "the {{ kind.name|lower }}, and what attendees will learn.</h4>"
)


SECTION2_LEGEND = (
    "<h4>The following fields are for the review process "
    "but are optional and will not be published publicly.</h4>"
)


SECTION3_LEGEND = (
    "<h4>Additionally, we will ask you some optional questions "
    "that will not be part of the review process and "
    "will not be published publicly.</h4>"
)


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
    class Meta:
        model = Proposal
        fields = [
            "title",
            "audience_level",
            "description",
            "abstract",
            "affiliation",
            "additional_notes",
            "first_time_at_jupytercon",
            "requests",
            "gender",
            "referral",
            "under_represented_group",
            "accomodation_needs",
            "recording_release",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                SECTION1_LEGEND,
                "title",
                "audience_level",
                "description",
                "abstract",
                "affiliation",
            ),
            Fieldset(
                SECTION2_LEGEND,
                "additional_notes",
                "first_time_at_jupytercon",
            ),
            Fieldset(
                SECTION3_LEGEND,
                "requests",
                "gender",
                "referral",
                "under_represented_group",
                "accomodation_needs",
            ),
            "recording_release",
            "phone_number",
        )

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value


class TutorialForm(ProposalForm):
    class Meta:
        model = Proposal
        fields = [
            "title",
            "audience_level",
            "target_audience",
            "description",
            "tutorial_format",
            "abstract",
            "affiliation",
            "additional_notes",
            "first_time_at_jupytercon",
            "requests",
            "gender",
            "referral",
            "under_represented_group",
            "accomodation_needs",
            "recording_release",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make Tutorial-specific fields required.
        # Since these fields aren't required for talks, they
        # can't be defined in the Proposal model.
        self.fields["target_audience"].required = True
        self.fields["tutorial_format"].required = True

        # Update Tutorial-specific help text.
        self.fields["title"].help_text = (
            "A clear title should convey "
            "in a few words what your tutorial is about."
        )
        self.fields["abstract"].help_text = (
            "Your outline should list the topics and activities you will "
            "guide your students through during your 3-hour tutorial."
        )
        self.fields["affiliation"].help_text = (
            "For the purpose of this tutorial."
        )
        self.fields["additional_notes"].help_text = (
            "Please summarize your teaching or public speaking experience, "
            "as well as your experience with the subject of the tutorial."
        )

        self.helper.layout = Layout(
            Fieldset(
                SECTION1_LEGEND,
                "title",
                "audience_level",
                "target_audience",
                "description",
                "tutorial_format",
                "abstract",
                "affiliation",
            ),
            Fieldset(
                SECTION2_LEGEND,
                "additional_notes",
                "first_time_at_jupytercon",
            ),
            Fieldset(
                SECTION3_LEGEND,
                "requests",
                "gender",
                "referral",
                "under_represented_group",
                "accomodation_needs",
            ),
            "recording_release",
            "phone_number",
        )


class PosterForm(ProposalForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update Poster-specific help text.
        self.fields["title"].help_text = (
            "A clear title should convey "
            "in a few words what your poster is about."
        )
        self.fields["affiliation"].help_text = (
            "For the purpose of this poster."
        )
