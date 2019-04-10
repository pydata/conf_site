# -*- coding: utf-8 -*-
import factory

from symposion.schedule.tests.factories import (
    ProposalKindFactory,
    SectionFactory,
)
from symposion.speakers.models import Speaker

from conf_site.accounts.tests.factories import UserFactory
from conf_site.proposals.models import Proposal


class SpeakerFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")

    class Meta:
        model = Speaker


class ProposalFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("bs")
    description = factory.Faker("paragraph")
    abstract = factory.Faker("paragraph")
    kind = factory.SubFactory(ProposalKindFactory)
    speaker = factory.SubFactory(SpeakerFactory)
    audience_level = factory.Faker("pyint")

    class Meta:
        model = Proposal
