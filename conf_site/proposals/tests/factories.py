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
    audience_level = factory.Faker("pyint")
    audience_background = factory.Faker("sentence")
    outline = factory.Faker("paragraph")

    class Meta:
        model = Proposal
