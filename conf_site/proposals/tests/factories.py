# -*- coding: utf-8 -*-
import factory

from symposion.schedule.tests.factories import ProposalKindFactory

from conf_site.proposals.models import Proposal
from conf_site.speakers.tests.factories import SpeakerFactory


class ProposalFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("bs")
    description = factory.Faker("paragraph")
    abstract = factory.Faker("paragraph")
    kind = factory.SubFactory(ProposalKindFactory)
    speaker = factory.SubFactory(SpeakerFactory)
    prior_knowledge = factory.Faker(
        "pystr_format", string_format="?", letters="NY"
    )

    class Meta:
        model = Proposal
