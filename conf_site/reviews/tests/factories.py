# -*- coding: utf-8 -*-
import factory

from conf_site.accounts.tests.factories import UserFactory
from conf_site.proposals.tests.factories import ProposalFactory
from conf_site.reviews.models import ProposalFeedback, ProposalVote


class ProposalFeedbackFactory(factory.django.DjangoModelFactory):
    proposal = factory.SubFactory(ProposalFactory)
    author = factory.SubFactory(UserFactory)
    comment = factory.Faker("paragraph")

    class Meta:
        model = ProposalFeedback


class ProposalVoteFactory(factory.django.DjangoModelFactory):
    proposal = factory.SubFactory(ProposalFactory)
    voter = factory.SubFactory(UserFactory)
    score = factory.fuzzy.FuzzyChoice(
        ProposalVote.SCORES, getter=lambda s: s[0]
    )
    comment = factory.Faker("paragraph")

    class Meta:
        model = ProposalVote
