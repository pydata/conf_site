from django.contrib import admin


from conf_site.reviews.models import ProposalVote


@admin.register(ProposalVote)
class ProposalVoteAdmin(admin.ModelAdmin):
    list_display = ("proposal", "voter", "score", "comment")
