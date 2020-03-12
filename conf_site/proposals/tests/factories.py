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
    target_audience = factory.Faker("sentence")
    tutorial_format = factory.Faker("sentence")
    first_time_at_jupytercon = factory.Iterator(
        Proposal.YES_NO_OTHER_ANSWERS, getter=lambda c: c[0]
    )
    affiliation = factory.Faker("sentence")
    requests = factory.Faker("sentence")
    gender = factory.Faker("sentence")
    referral = factory.Faker("sentence")
    under_represented_group = factory.Faker("sentence")
    accomodation_needs = factory.Faker("sentence")

    class Meta:
        model = Proposal
