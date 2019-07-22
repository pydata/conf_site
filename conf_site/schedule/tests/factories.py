# -*- coding: utf-8 -*-
import factory

from symposion.schedule.models import Presentation
from symposion.schedule.tests.factories import SectionFactory, SlotFactory

from conf_site.proposals.tests.factories import ProposalFactory, SpeakerFactory


class PresentationFactory(factory.django.DjangoModelFactory):
    title = factory.faker.Faker("catch_phrase")
    slot = factory.SubFactory(SlotFactory)
    speaker = factory.SubFactory(SpeakerFactory)
    proposal_base = factory.SubFactory(ProposalFactory)
    section = factory.SubFactory(SectionFactory)

    class Meta:
        model = Presentation
