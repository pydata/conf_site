# -*- coding: utf-8 -*-
from django import forms

from conf_site.reviews.models import (
    ProposalFeedback,
    ProposalNotification,
    ProposalVote,
)


class ProposalVoteForm(forms.ModelForm):
    class Meta:
        model = ProposalVote
        fields = ["score", "comment"]

    def __init__(self, *args, **kwargs):
        super(ProposalVoteForm, self).__init__(*args, **kwargs)
        # Use a radio select widget instead of a dropdown for the score.
        self.fields["score"] = forms.TypedChoiceField(
            choices=ProposalVote.SCORES,
            coerce=int,
            empty_value=0,
            widget=forms.RadioSelect(),
        )


class ProposalFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProposalFeedback
        fields = ["comment"]


class ProposalNotificationForm(forms.ModelForm):
    class Meta:
        model = ProposalNotification
        fields = ["from_address", "subject", "body"]
