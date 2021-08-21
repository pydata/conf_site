from django.contrib import admin

from conf_site.proposals.models import Proposal, ProposalKeyword, ProposalTrack


class ProposalAdditionalSpeakerThrough(Proposal.additional_speakers.through):
    """https://stackoverflow.com/a/4929036/113527"""
    class Meta:
        proxy = True
        verbose_name = "Additional Speaker"

    def __str__(self):
        return ""


class AdditionalSpeakerInline(admin.TabularInline):
    extra = 0
    model = ProposalAdditionalSpeakerThrough
    verbose_name = "additional speaker"


@admin.register(ProposalKeyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "official",)
    list_filter = ("official",)


@admin.register(ProposalTrack)
class ProposalTrackAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    inlines = [AdditionalSpeakerInline]
    list_display = (
        'number',
        'title',
        'speaker',
        'kind',
        'prior_knowledge',
        'cancelled',
        "date_created",
        "date_last_modified",
    )
    list_display_links = ("title",)
    list_filter = (
        'kind',
        'prior_knowledge',
        'cancelled',
        'recording_release',
    )
    search_fields = ("title", "speaker__name")
    date_hierarchy = "date_created"
