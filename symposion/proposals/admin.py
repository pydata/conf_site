from django.contrib import admin

from symposion.proposals.models import ProposalSection, ProposalKind


class ProposalKindAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "section", "order"]
    list_editable = ["slug", "order"]
    list_filter = ["section"]


class ProposalSectionAdmin(admin.ModelAdmin):
    list_display = [
        "section",
        "start",
        "end",
        "closed",
        "published",
        "available",
    ]


admin.site.register(ProposalSection, ProposalSectionAdmin)
admin.site.register(ProposalKind, ProposalKindAdmin)
