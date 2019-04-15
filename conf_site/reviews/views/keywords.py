from itertools import chain

from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from conf_site.proposals.models import Proposal, ProposalKeyword


class ReviewKeywordListView(ListView):
    """A view to display keywords associated with proposals for reviewers."""
    context_object_name = "keywords"
    template_name = "reviews/proposalkeyword_list.html"

    def get_queryset(self, **kwargs):
        return ProposalKeyword.objects.all().order_by("name")


class ReviewKeywordDetailView(ListView):
    """A view that displays proposals associated with a specific keyword."""
    context_object_name = "proposal_list"
    template_name = "reviews/keyword_detail.html"

    def get(self, request, *args, **kwargs):
        # Save keyword from slug.
        keyword_slug = kwargs.get("keyword_slug")
        self.keyword = get_object_or_404(ProposalKeyword, slug=keyword_slug)
        return super(ReviewKeywordDetailView, self).get(
            request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        # Merge querysets for editor keywords, official keywords,
        # and user tagged keywords into one big list, sorted by
        # proposal ID.
        editor_proposals = Proposal.objects.filter(
            editor_keywords__id__in=[self.keyword.id])
        official_proposals = Proposal.objects.filter(
            official_keywords__id__in=[self.keyword.id])
        user_proposals = Proposal.objects.filter(
            user_keywords__id__in=[self.keyword.id])
        return sorted(
            chain(editor_proposals, official_proposals, user_proposals),
            key=lambda instance: instance.id)

    def get_context_data(self, **kwargs):
        """Add keyword to template context."""
        context = super(
            ReviewKeywordDetailView, self).get_context_data(**kwargs)
        context["keyword"] = self.keyword
        return context
