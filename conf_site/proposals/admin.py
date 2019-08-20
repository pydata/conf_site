from django.contrib import admin

from conf_site.proposals.models import Proposal, ProposalKeyword


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


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    exclude = (
        "under_represented_population",
        "under_represented_details",
        "under_represented_other",
    )
    inlines = [AdditionalSpeakerInline]
    list_display = (
        'number',
        'title',
        'speaker',
        'kind',
        'audience_level',
        'cancelled',
        "date_created",
        "date_last_modified",
    )
    list_display_links = ("title",)
    search_fields = ("title", "speaker__name")
    date_hierarchy = "date_created"

    def get_list_filter(self, request):
        list_filter = (
            "kind",
            "audience_level",
            "cancelled",
            "recording_release",
        )
        if request.user.is_superuser:
            list_filter += ("travel_stipend",)
        return list_filter
