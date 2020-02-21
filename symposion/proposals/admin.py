from django.contrib import admin

from symposion.proposals.models import ProposalSection, ProposalKind


class ProposalSectionAdmin(admin.ModelAdmin):
    list_display = [
        "section",
        "start",
        "end",
        "closed",
        "published",
        "is_available",
    ]


admin.site.register(ProposalSection, ProposalSectionAdmin)
admin.site.register(ProposalKind)
