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
    commitment = factory.Faker("boolean")
    mentorship = factory.Faker("boolean")
    company_sponsor_intro = factory.Faker("boolean")

    class Meta:
        model = Proposal
