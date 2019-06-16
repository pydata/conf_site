from django.contrib import admin

from symposion.proposals.models import ProposalSection, ProposalKind


admin.site.register(ProposalSection)
admin.site.register(ProposalKind)
