from django.contrib import admin

from conf_site.reviews.models import (
    ProposalFeedback,
    ProposalNotification,
    ProposalResult,
    ProposalVote,
)


class ProposalInline(admin.StackedInline):
    model = ProposalNotification.proposals.through


@admin.register(ProposalFeedback)
class ProposalFeedbackAdmin(admin.ModelAdmin):
    list_display = ("proposal", "author", "comment", "date_created")


@admin.register(ProposalNotification)
class ProposalNotificationAdmin(admin.ModelAdmin):
    exclude = ("proposals",)
    inlines = [ProposalInline]
    list_display = ("subject", "body", "date_sent")


@admin.register(ProposalResult)
class ProposalResultAdmin(admin.ModelAdmin):
    list_display = ("proposal", "status")


@admin.register(ProposalVote)
class ProposalVoteAdmin(admin.ModelAdmin):
    list_display = ("proposal", "voter", "score", "comment")
    list_filter = ["score", "voter"]
