import datetime
import random

from factory import faker, fuzzy, SubFactory
from factory.django import DjangoModelFactory

from symposion.schedule.models import Schedule, Day, Slot, SlotKind
from symposion.conference.models import Section, Conference
from symposion.proposals.models import ProposalKind


class ConferenceFactory(DjangoModelFactory):
    title = fuzzy.FuzzyText()
    start_date = fuzzy.FuzzyDate(datetime.date(2014, 1, 1))
    end_date = fuzzy.FuzzyDate(
        datetime.date(2014, 1, 1)
        + datetime.timedelta(days=random.randint(1, 10))
    )

    class Meta:
        model = Conference


class SectionFactory(DjangoModelFactory):
    conference = SubFactory(ConferenceFactory)
    name = fuzzy.FuzzyText()
    slug = fuzzy.FuzzyText()

    class Meta:
        model = Section


class ProposalKindFactory(DjangoModelFactory):
    section = SubFactory(SectionFactory)
    name = fuzzy.FuzzyText()
    slug = fuzzy.FuzzyText()
    order = fuzzy.FuzzyInteger(0, 100)

    class Meta:
        model = ProposalKind


class ScheduleFactory(DjangoModelFactory):
    section = SubFactory(SectionFactory)
    published = True
    hidden = False

    class Meta:
        model = Schedule


class SlotKindFactory(DjangoModelFactory):
    schedule = SubFactory(ScheduleFactory)
    label = fuzzy.FuzzyText()

    class Meta:
        model = SlotKind


class DayFactory(DjangoModelFactory):
    schedule = SubFactory(ScheduleFactory)
    date = fuzzy.FuzzyDate(datetime.date(2014, 1, 1))

    class Meta:
        model = Day


fake_tzinfo = faker.faker.Faker().pytimezone()


class SlotFactory(DjangoModelFactory):
    day = SubFactory(DayFactory)
    kind = SubFactory(SlotKindFactory)
    start = faker.Faker("past_datetime", tzinfo=fake_tzinfo)
    end = faker.Faker("future_datetime", tzinfo=fake_tzinfo)

    class Meta:
        model = Slot
