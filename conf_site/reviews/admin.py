from django.contrib import admin


from conf_site.reviews.models import ProposalFeedback, ProposalVote


@admin.register(ProposalFeedback)
class ProposalFeedbackAdmin(admin.ModelAdmin):
    list_display = ("proposal", "author", "comment", "date_created")


@admin.register(ProposalVote)
class ProposalVoteAdmin(admin.ModelAdmin):
    list_display = ("proposal", "voter", "score", "comment")
