from django.contrib import admin

from .models import TalkProposal, TutorialProposal


@admin.register(TalkProposal, TutorialProposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'title',
        'speaker_email',
        'speaker',
        'kind',
        'audience_level',
        'cancelled',
    )
    list_filter = (
        'kind',
        'audience_level',
        'cancelled',
        'recording_release',
    )
    date_heirarchy = 'submitted'
